import os
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant, FAISS
import openai
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils import read_pdf
from langchain.schema import Document
import logging

from dotenv import dotenv_values

ae_doc_path = "../assets/Arabic Executive Regulation Law No 6-2016.pdf"
en_doc_path = "../assets/law-english.pdf"
class DocumentProcessor:
    """Handles augmenting our document and generating embeddings"""
    def __init__(self):
        self._embeddingsModel = OpenAIEmbeddings(api_key=dotenv_values("../.env").get("OPENAI_API_KEY"))
        self._splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", r"(?<=[.?!])\s+"],
            keep_separator=False,
            is_separator_regex=True,
            chunk_size=1000,
            chunk_overlap=0
        )
    
    def document_augmentation(self, documentPath: str) -> list[Document]:
        """Splits the document into chunks ready to be embedded"""
        document = read_pdf(documentPath)
        logging.info(f"Document read from path: {documentPath}")

        documentChunks = self._splitter.split_text(document)
        print(f"Document split into {len(documentChunks)} chunks.")
        #these document chunks dont have a page content attribute so we need to do it using langchains document schema
        return [Document(page_content=text) for text in documentChunks]
    
    def generate_embeddings(self, documentObjects: list[Document]) -> None:
        """Generates embeddings for each document chunk, this uses openai to do so"""
        for doc in documentObjects:
            try:
                self._embeddingsModel.embed_documents([doc.page_content])
                print(f"Embedding for document chunk: {doc.page_content[:30]}... created.")
            except Exception as e:
                print(f"Error creating embedding: {e}")
        return self._embeddingsModel  # Return all embeddings
    
class DocumentStorage:
    """Handles storing the embeddings in the database"""
    def __init__(self):
        self._client = QdrantClient("http://localhost:6333")

    def is_database_populated(self) -> bool:
        """Checks if the database is already populated"""
        count = self._client.count(collection_name="my_documents")
        print(count)

    def store_embeddings(self, embeddings: list[list[float]], documentChunks: list[str], collectionName) -> None:
        """Stores the embeddings in the vector database"""
        client = QdrantClient("http://localhost:6333")
        vector_db = Qdrant.from_documents(documentChunks, embeddings, collection_name=collectionName)
        return
    
class DocumentHandler:
    """Coordinates document processing and storage."""
    def __init__(self, collectionName: str):
        self.processor = DocumentProcessor()
        self.storage = DocumentStorage()
        self._collectionName = collectionName

    def process_and_store(self, document_path: str) -> None:
        """End-to-end processing: document augmentation, embedding generation, and pushing to Qdrant."""

        document_chunks = self.processor.document_augmentation(document_path)
        embeddings = self.processor.generate_embeddings(document_chunks)

        if embeddings:
            self.storage.store_embeddings(embeddings, document_chunks, self._collectionName)

if __name__ == "__main__":
    print()
    # handler = DocumentHandler("en_doc")
    # handler.process_and_store(en_doc_path)
