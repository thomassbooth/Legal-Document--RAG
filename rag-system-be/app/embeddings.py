import os
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant, FAISS
import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import read_pdf
from langchain.schema import Document

ae_doc_path = "./assets/Arabic Executive Regulation Law No 6-2016.pdf"
en_doc_path = "./assets/law-english.pdf"

# Document augmentation and indexing
def augment_and_index_documents(document_path, index_type="qdrant"):
    # Load the document
    document = read_pdf(document_path)

    # Split the document into chunks
    # https://www.analyticsvidhya.com/blog/2024/07/langchain-text-splitters/
    splitter = RecursiveCharacterTextSplitter(
                  separators=["\n\n", "\n", r"(?<=[.?!])\s+"],                                   
                  keep_separator=False, is_separator_regex=True,
                  chunk_size=30, chunk_overlap=0)
    document_chunks = splitter.split_text(document)

    document_objects = [Document(page_content=text) for text in document_chunks]

    # embeddings = OpenAIEmbeddings()

    # embeddings = OpenAIEmbeddings(openai_api_key=apikey)

    # for doc in document_objects:
    #     try:
    #         embedding = embeddings.embed_documents([doc.page_content])
    #         print(f"Embedding for document chunk: {doc.page_content[:30]}... created.")
    #     except Exception as e:
    #         print(f"Error creating embedding: {e}")

    # print(embeddings)


    client = QdrantClient("http://localhost:6333")
    count = client.count(collection_name="my_documents")
    print(count)
    # vector_db = Qdrant.from_documents(document_objects, embeddings, collection_name="my_documents")
    # # Initialize vector index based on chosen system (Qdrant or FAISS)
    # if index_type == "qdrant":
    #     client = QdrantClient(":memory:")  # Using in-memory instance of Qdrant
    #     vector_db = Qdrant.from_documents(document_chunks, embeddings, client=client, collection_name="my_documents")
    # elif index_type == "faiss":
    #     vector_db = FAISS.from_documents(document_chunks, embeddings)

    return 

if "__main__" == __name__:
    print('hi')
    augment_and_index_documents(en_doc_path)