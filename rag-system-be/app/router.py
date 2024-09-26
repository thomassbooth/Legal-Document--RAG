from fastapi import WebSocket, APIRouter

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        response = "test"
        for chunk in response:
            await websocket.send_text(chunk)


@router.get("/")
async def check_database_populated():
    return {"message": "Hello World"}