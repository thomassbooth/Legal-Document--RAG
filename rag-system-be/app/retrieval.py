from langdetect import detect
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant, FAISS
from dotenv import dotenv_values
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.retrievers.multi_query import MultiQueryRetriever

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# steps to take
# Convert my user query into an embedding vector, this way we can match what we have in the vector database
#
#
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

def query_vectorstore(query, language):

    retriever = MultiQueryRetriever.from_llm(retriever=en_vectorstore.as_retriever(search_type="similarity", search_kwargs = {"k":  10}), llm = llm)
    
    # Retrieve documents using MultiQueryRetriever
    retrieved_docs = retriever.invoke(query)
    print(f"Number of retrieved documents: {len(retrieved_docs)}")
    print(f"First retrieved document content: {retrieved_docs[0].page_content if retrieved_docs else 'No documents found.'}")
    
    # Format the retrieved documents into a string
    context_str = format_docs(retrieved_docs)

    # Load the LLM prompt template
    prompt = hub.pull("rlm/rag-prompt")
    example_messages = prompt.invoke(
        {"context": "filler context", "question": "filler question"}
    ).to_messages()

    print(f"Example message: {example_messages[0].content}")

    # Create the rag_chain
    rag_chain = (
        {"context": RunnablePassthrough(), "question": RunnablePassthrough()}  # Adjusting to work with the chain
        | prompt
        | llm
        | StrOutputParser()
    )

    # Stream the results using the formatted context and user query
    print("Streaming results:")
    for chunk in rag_chain.stream({"context": context_str, "question": query}):
        print(chunk, end="", flush=True)


if __name__ == "__main__":
    query = "What are the commitments and responsibilities of government agencies regarding employee management and development?"
    query_type = get_query_type(query)
    print(query_vectorstore(query, query_type))
