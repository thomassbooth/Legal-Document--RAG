from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from .retrieval import query_vectorstore
from .connections import ConnectionManager
router = APIRouter()


manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Stream results back to the WebSocket
            query = data  # Assuming 'data' contains the query

            # Stream results back to the WebSocket
            await query_vectorstore(query, "en", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)


@router.get("/")
async def check_database_populated():
    return {"message": "Hello World"}
