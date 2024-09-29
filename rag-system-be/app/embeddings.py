import os
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .utils import read_pdf
from langchain.schema import Document
import logging

from dotenv import dotenv_values

ae_doc_path = "../assets/ar-law.pdf"
en_doc_path = "../assets/en-law.pdf"


class DocumentProcessor:
    """Handles augmenting our document and generating embeddings"""

    def __init__(self):
        apikey = os.environ.get("OPENAI_API_KEY")
        if apikey is None:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self._embeddingsModel = OpenAIEmbeddings(
            api_key=apikey)
        self._splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", r"(?<=[.?!])\s+"],
            keep_separator=False,
            is_separator_regex=True,
            chunk_size=700,
            chunk_overlap=200
        )

    def document_augmentation(self, documentPath: str) -> list[Document]:
        """Splits the document into chunks ready to be embedded"""
        document = read_pdf(documentPath)
        logging.info(f"Document read from path: {documentPath}")

        documentChunks = self._splitter.split_text(document)
        print(f"Document split into {len(documentChunks)} chunks.")
        # these document chunks dont have a page content attribute so we need to do it using langchains document schema
        return [Document(page_content=text) for text in documentChunks]

    def generate_embeddings(self, documentObjects: list[Document]) -> OpenAIEmbeddings:
        """Generates embeddings for each document chunk, this uses openai to do so"""
        for doc in documentObjects:
            try:
                # Embed the document chunk
                self._embeddingsModel.embed_documents([doc.page_content])
                print(
                    f"Embedding for document chunk: {doc.page_content[:30]}... created.")
            except Exception as e:
                print(f"Error creating embedding: {e}")
        return self._embeddingsModel  # Return all embeddings


class DocumentStorage:
    """Handles storing the embeddings in the database"""

    def __init__(self):
        self._qdrantUrl = os.environ.get("QDRANT_CLIENT")
        self._client = QdrantClient(self._qdrantUrl)

    def is_database_populated(self, collectionName) -> bool:
        """Checks if the database is already populated"""
        try:
            count = self._client.count(collection_name=collectionName)
            print(count)
            return count.count > 0
        except Exception as err:
            return False

    def store_embeddings(self, embeddings: list[list[float]], documentChunks: list[str], collectionName) -> None:
        """Stores the embeddings in the vector database"""
        try:
            # count = self._client.count(collection_name=collectionName)
            #put the embeddings in the database under the passed collection name
            vectorDb = Qdrant.from_documents(
                documentChunks, embeddings, url = self._qdrantUrl, collection_name=collectionName)
        except Exception as error:
            print(f"Error storing embeddings: {error}")
            if isinstance(error, ConnectionError):
                print("Failed to connect to Qdrant. Please check the server address and network settings.")
            elif isinstance(error, TimeoutError):
                print("Request to Qdrant timed out. Please check if the server is running and reachable.")
            else:
                print("An unexpected error occurred.")
        return


class DocumentHandler:
    """Coordinates document processing and storage."""

    def __init__(self, collectionName: str):
        self.processor = DocumentProcessor()
        self.storage = DocumentStorage()
        self._collectionName = collectionName

    def process_and_store(self, document_path: str) -> None:
        """End-to-end processing: document augmentation, embedding generation, and pushing to Qdrant."""

        documentChunks = self.processor.document_augmentation(document_path)
        embeddings = self.processor.generate_embeddings(documentChunks)

        if embeddings:
            self.storage.store_embeddings(
                embeddings, documentChunks, self._collectionName)
            
    def get_is_populated(self):
        """Checks if the database is already populated"""
        return self.storage.is_database_populated(self._collectionName)
        

    

if __name__ == "__main__":
    print()
    handler = DocumentHandler("ar_doc111")
    handler.process_and_store(ae_doc_path)
