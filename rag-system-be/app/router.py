from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from .connections import ConnectionManager
from .retrieval import EmbeddingModelLoader, VectorStoreManager, MemoryManager, QueryProcessor
from qdrant_client import QdrantClient
from dotenv import dotenv_values
import json

router = APIRouter()


manager = ConnectionManager()
api_key = dotenv_values("../.env").get("OPENAI_API_KEY")
embedding_loader = EmbeddingModelLoader(api_key)

# Initialize vector store manager and memory manager
qdrant_client = QdrantClient("http://qdrant:6333")
vector_manager = VectorStoreManager(
    qdrant_client, embedding_loader.get_model())
memory_manager = MemoryManager()

# Initialize Query Processor
query_processor = QueryProcessor(
    embedding_loader, vector_manager, memory_manager)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            query = json.loads(data) 
            if query.get("message") == None or query.get("userid") == None:
                await manager.send_message("We cannot identify you! Please provide a valid user id.")

            await manager.send_message(query_processor.process_query(query["message"], query["userid"]))

    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.get("/")
async def check_database_populated():
    return {"message": "Hello World"}
