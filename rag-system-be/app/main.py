from fastapi import FastAPI
from .router import router
from contextlib import asynccontextmanager
from .embeddings import DocumentHandler
import asyncio


#using the context manager, on startup of the app before the server is started, we can run some expensive processes
@asynccontextmanager
async def lifespan(app: FastAPI):
    print('setting up ML models')
    handler = DocumentHandler("en_doc")
    handler.process_and_store(en_doc_path)

    # These processes are expensive, so running on two different threads cuts the startup time in half
    # concurrently create embeddings for both documents and upload to the database
    task1 = asyncio.create_task(handler.process_and_store(en_doc_path))

    task2 = asyncio.create_task(w)
    # yield is used here to pause the execution of the app, allowing us to clean up resources
    yield
    

app = FastAPI(lifespan=lifespan)

app.include_router(router)
