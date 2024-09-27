from fastapi import FastAPI
from .router import router
from contextlib import asynccontextmanager
from .embeddings import DocumentHandler
from .utils import get_assets_file_path
from qdrant_client import QdrantClient
import asyncio
import os

#using the context manager, on startup of the app before the server is started, we can run some expensive processes
@asynccontextmanager
async def lifespan(app: FastAPI):

    client = QdrantClient("http://qdrant:6333")
    count = client.count(collection_name="en_doc")
    print(count)
    # print('setting up DB for queries')
    # handlerEn = DocumentHandler("en_doc")
    handlerAr = DocumentHandler("test")
    # #get our paths
    # enPath = get_assets_file_path("en-law.pdf")
    arPath = get_assets_file_path("en-law.pdf")
    # # These processes are expensive, so running on two different threads cuts the startup time in half
    # # concurrently create embeddings for both documents and upload to the database
    handlerAr.process_and_store(arPath)
    # # arDocThread = asyncio.create_task(handlerAr.process_and_store(arPath))
    
    # #wait for our two threads to finish their processes so we can boot up the server
    # # await asyncio.gather(enDocThread, arDocThread)
    # # yield is used here to pause the execution of the app, allowing us to clean up resources on close
    yield
    

app = FastAPI(lifespan=lifespan)

app.include_router(router)
