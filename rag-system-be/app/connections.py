from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    def __init__(self):
        self.activeConnections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.activeConnections.append(websocket)
        await websocket.send_text("Hey! Nice to meet you, what can I help you with today?")

    def disconnect(self, websocket: WebSocket):
        self.activeConnections.remove(websocket)

    async def send_message(self, message: str):
        for connection in self.activeConnections:
            await connection.send_text(message)
