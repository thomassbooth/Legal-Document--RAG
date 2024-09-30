from langdetect import detect
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from dotenv import dotenv_values
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from fastapi import WebSocket

# steps to take
# Convert my user query into an embedding vector, this way we can match what we have in the vector database
# https://python.langchain.com/docs/tutorials/rag/#indexing-load
# https://python.langchain.com/docs/how_to/MultiQueryRetriever/


class LanguageDetector:
    """Detects the language of a given query"""
    @staticmethod
    def detect_language(query: str) -> str:
        try:
            lang = detect(query)
            if lang in ["ar", "en"]:
                return lang
            raise ValueError(f"Unsupported language: {lang}")
        except Exception as err:
            raise ValueError(f"Error detecting language: {err}")


class EmbeddingModelLoader:
    """Loads the OpenAI Embeddings model"""

    def __init__(self, api_key: str):
        self.embeddingModel = OpenAIEmbeddings(api_key=api_key)

    def get_model(self):
        return self.embeddingModel


class VectorStoreManager:
    """Manages the vector store based on the language"""

    def __init__(self, qdrant_client: QdrantClient, embedding_model: OpenAIEmbeddings):
        self._enVectorstore = Qdrant(
            client=qdrant_client, collection_name="en_doc", embeddings=embedding_model)
        self._arVectorstore = Qdrant(
            client=qdrant_client, collection_name="ar_doc", embeddings=embedding_model)

    def get_vectorstore(self, language: str) -> Qdrant:
        """Retrieve the vector store based on the language"""
        if language == "en":
            return self._enVectorstore
        elif language == "ar":
            return self._arVectorstore
        else:
            raise ValueError(f"Unsupported language: {language}")


class MemoryManager:
    """For ecah user we want to store their memory, this should be in a database but for simplicity i use a map"""

    def __init__(self):
        # Store memory for each user based on user ID
        self.user_memories = {}

    def _get_user_memory(self, user_id: str) -> ConversationBufferMemory:
        """Retrieve or initialize a ConversationBufferMemory for the given user_id."""
        if user_id not in self.user_memories:
            self.user_memories[user_id] = ConversationBufferMemory()
        return self.user_memories[user_id]

    def get_chat_history(self, user_id: str) -> str:
        """Retrieve chat history for a specific user."""
        userMemory = self._get_user_memory(user_id)
        memoryVars = userMemory.load_memory_variables({})
        return memoryVars

    def save_chat_context(self, user_id: str, query: str, response: str):
        """Save the conversation context for a specific user."""
        userMemory = self._get_user_memory(user_id)
        userMemory.save_context({"input": query}, {"output": response})


class QueryProcessor:
    """Processes the user query and retrieves relevant documents"""

    def __init__(self, embedding_model_loader: EmbeddingModelLoader, vectorstore_manager: VectorStoreManager, memory_manager: MemoryManager):
        self._embedding_model_loader = embedding_model_loader
        self._vectorstore_manager = vectorstore_manager
        self._memory_manager = memory_manager
        self._llm = ChatOpenAI(
            model="gpt-4o-mini", api_key=dotenv_values("../.env").get("OPENAI_API_KEY"), max_tokens=1500)

    @staticmethod
    def _format_docs(docs):
        """Format retrieved documents into a single string"""
        return "\n\n".join(doc.page_content for doc in docs)

    async def process_query(self, query: str, userid: int, ws: WebSocket):
        """Process and query the vector store based on the language and query"""
        print('inside process query')
        try:
            language = LanguageDetector.detect_language(query)
        except:
            error_message = "Please type your query in either Arabic or English, thank you!"
            await ws.send_text("start+")
            await ws.send_text(error_message)
            await ws.send_text("end+")
            return
        # Retrieve conversation history from memory
        chatHistory = self._memory_manager.get_chat_history(userid)
        fullQuery = f"{chatHistory.get('history', '')}\n\nUser: {query}"

        # Select vector store based on the language
        vectorstore = self._vectorstore_manager.get_vectorstore(language)
        # Use a multiquery retriever to generate multiple prompts, grab docs then combine the result
        retriever = MultiQueryRetriever.from_llm(retriever=vectorstore.as_retriever(
            search_type="similarity", search_kwargs={"k": 10}), llm=self._llm)

        # Load the prompt template from the hub
        prompt = hub.pull("rlm/rag-prompt")

        # Create the RAG chain, this essentially pipes each part as its computed as it goes through the chain
        ragChain = (
            # Adjusting to work with the chain
            {"context": retriever | self._format_docs,
                "question": RunnablePassthrough()}
            | prompt
            | self._llm
            | StrOutputParser()
        )

        # Stream the results using the formatted context and user query this is an async generator, so no need to use yield
        finalResponse = ""
        first = True
        async for chunk in ragChain.astream({"question": fullQuery}):
            if first:
                first = False
                await ws.send_text("start+")
            finalResponse += chunk
            await ws.send_text(chunk)

        await ws.send_text("end+")
        # Save the conversation context in memory
        self._memory_manager.save_chat_context(userid, query, finalResponse)

        # return finalResponse


if __name__ == "__main__":
    api_key = dotenv_values("../.env").get("OPENAI_API_KEY")
    embedding_loader = EmbeddingModelLoader(api_key)

    # Initialize vector store manager and memory manager
    qdrant_client = QdrantClient("http://localhost:6333")
    vector_manager = VectorStoreManager(
        qdrant_client, embedding_loader.get_model())
    memory_manager = MemoryManager()

    # Initialize Query Processor
    query_processor = QueryProcessor(
        embedding_loader, vector_manager, memory_manager)

    # Example queries
    queries = ["What are the rights of an employee?",
               "What are the implications of leaving a company?"]

    for query in queries:
        query_processor.process_query(query)
