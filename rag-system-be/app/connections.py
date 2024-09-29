from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    """Manages active websocket connections"""
    def __init__(self):
        self.activeConnections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.activeConnections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.activeConnections.remove(websocket)

    async def send_message(self, message: str):
        for connection in self.activeConnections:
            await connection.send_text(message)
