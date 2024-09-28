from langdetect import detect
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant, FAISS
from dotenv import dotenv_values
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# steps to take
# Convert my user query into an embedding vector, this way we can match what we have in the vector database
# https://python.langchain.com/docs/tutorials/rag/#indexing-load
# https://python.langchain.com/docs/how_to/MultiQueryRetriever/

embedding_model = OpenAIEmbeddings(
    api_key=dotenv_values("../.env").get("OPENAI_API_KEY"))
qdrant_client = QdrantClient("http://localhost:6333")
en_vectorstore = Qdrant(client=qdrant_client,
                        collection_name="en_doc", embeddings=embedding_model)
ar_vectorstore = Qdrant(client=qdrant_client,
                        collection_name="ar_doc", embeddings=embedding_model)

llm = ChatOpenAI(model="gpt-4o-mini",
                 api_key=dotenv_values("../.env").get("OPENAI_API_KEY"),
                 max_tokens=1500)

memory = ConversationBufferMemory()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def get_query_type(query: str) -> str:
    """Detect language of the query, you can only query in arabic or english"""
    try:
        lang = detect(query)
        if lang == "ar" or lang == "en":
            return lang
        else:
            raise ValueError(f"Unsupported language: {lang}")
    except Exception as err:
        raise ValueError(f"Error detecting language: {err}")

def query_vectorstore(query: str, language: str):

    memory_variables = memory.load_memory_variables({})
    chat_history = memory_variables.get('history', '')

    print("Chat history:", chat_history)

    # Combine chat history with the new user query
    full_query = f"{chat_history}\n\nUser: {query}"
    retriever = MultiQueryRetriever.from_llm(retriever=en_vectorstore.as_retriever(search_type="similarity", search_kwargs = {"k":  10}), llm = llm)
    
    # Load the LLM prompt template
    prompt = hub.pull("rlm/rag-prompt")
    # Create the rag_chain
    # retriever grabs the relevant documents, we use chaining here retriever is being passed into format_docs
    # question is just a place holder, these are passed into the prompt which is a structure to generate a final output
    # feeding into an llm
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}  # Adjusting to work with the chain
        | prompt
        | llm
        | StrOutputParser()
    )

    # Stream the results using the formatted context and user query
    print("Streaming results:")
    final_response = ""
    for chunk in rag_chain.stream({"question": full_query}):
        print(chunk, end="", flush=True)

        final_response += chunk
    memory.save_context({"question": query}, {"answer": final_response})


if __name__ == "__main__":
    query = "What are the rights of an employee?"
    query_vectorstore(query, "en")
    query = "What are the implications of leaving a company"
    query_type = get_query_type(query)
    query_vectorstore(query, "en")
