from fastapi import FastAPI
from .router import router
from contextlib import asynccontextmanager
from .embeddings import DocumentHandler
from .utils import get_assets_file_path
from qdrant_client import QdrantClient
import asyncio
import os
from fastapi.middleware.cors import CORSMiddleware


async def process_doc(handler, file):
    path = get_assets_file_path(file)
    loop = asyncio.get_running_loop()
    # Run the blocking process_and_store in a thread pool
    await loop.run_in_executor(None, handler.process_and_store, path)

@asynccontextmanager
async def lifespan(app: FastAPI):

    client = QdrantClient("http://qdrant:6333")
    # count = client.count(collection_name="en_doc")
    handlerEn = DocumentHandler("en_doc")
    handlerAr = DocumentHandler("ar_doc")

    #we only want to regenerate our embeddings if they are not already populated
    if (handlerAr.get_is_populated() == False and handlerEn.get_is_populated() == False):
        # Push off to other threads since these are expensive, cutting the runtime in two
        await asyncio.gather(process_doc(handlerEn, "en-law.pdf"),
                            process_doc(handlerAr, "ar-law.pdf"))

    # yield is used here to pause the execution of the app, allowing us to clean up resources on close
    yield

    print('server shutdown')


app = FastAPI(lifespan=lifespan)

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
