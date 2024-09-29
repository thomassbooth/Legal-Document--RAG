from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from .connections import ConnectionManager
from .retrieval import EmbeddingModelLoader, VectorStoreManager, MemoryManager, QueryProcessor, MemoryManager
from qdrant_client import QdrantClient
from dotenv import dotenv_values
import json
import os

router = APIRouter()

manager = ConnectionManager()
api_key = os.environ.get("OPENAI_API_KEY")
qdrant_url = os.environ.get("QDRANT_CLIENT")
embedding_loader = EmbeddingModelLoader(api_key)

# Initialize vector store manager and memory manager
qdrant_client = QdrantClient(qdrant_url)
vector_manager = VectorStoreManager(qdrant_client, embedding_loader.get_model())
memory_manager = MemoryManager()

# Initialize Query Processor
query_processor = QueryProcessor(embedding_loader, vector_manager, memory_manager)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            query = json.loads(data) 
            if query.get("message") == None or query.get("userid") == None:
                await manager.send_message("We cannot identify you! Please provide a valid user id.")
                await manager.disconnect(websocket)
                return

            await manager.send_message(query_processor.process_query(query["message"], query["userid"]))

    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.get("/user-history/{userid}")
async def get_user_history(userid: int):
    """Get the users history, if it exists else return a welcome message"""
    history = memory_manager.get_chat_history(userid)

    if history.get('history') == "":
        return {"history": [{"userType": 0, "data": "Hey nice to meet you! I am here to help you with any questions you have."}]}
    
    output = []
    for line in history.get('history', '').strip().split("\n"):
        if line.startswith("Human:"):
            output.append({"userType": 1, "data": line.replace("Human: ", "").strip()})
        elif line.startswith("AI:"):
            output.append({"userType": 0, "data": line.replace("AI: ", "").strip()})

    return {"history": output}
