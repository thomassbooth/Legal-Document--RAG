from fastapi import FastAPI
from .router import router
from contextlib import asynccontextmanager
from .embeddings import DocumentHandler
from .utils import get_assets_file_path
from qdrant_client import QdrantClient
import asyncio
import os
from fastapi.middleware.cors import CORSMiddleware


#using the context manager, on startup of the app before the server is started, we can run some expensive processes
@asynccontextmanager
async def lifespan(app: FastAPI):

    # client = QdrantClient("http://qdrant:6333")
    # # count = client.count(collection_name="en_doc")

    
    # #create new instances of our document handlers
    # handlerEn = DocumentHandler("en_doc")
    # handlerAr = DocumentHandler("ar_doc")
    # #get our paths
    # enPath = get_assets_file_path("en-law.pdf")
    # arPath = get_assets_file_path("en-law.pdf")
    # # These processes are expensive, so running on two different threads cuts the startup time in half
    # # concurrently create embeddings for both documents and upload to the database
    # handlerAr.process_and_store(arPath)
    # handlerEn.process_and_store(enPath)
    
    #yield is used here to pause the execution of the app, allowing us to clean up resources on close
    yield
    

app = FastAPI(lifespan=lifespan)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your actual frontend domain(s)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods, or restrict to specific methods like ['GET']
    allow_headers=["*"],  # Allow all headers, or restrict as necessary
)