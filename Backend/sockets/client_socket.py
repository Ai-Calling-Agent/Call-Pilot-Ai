from fastapi import WebSocket, WebSocketDisconnect

frontend_socket = None

async def handle_client_socket(websocket: WebSocket):
    global frontend_socket
    frontend_socket = websocket
    await websocket.accept()
    print("🟢 Frontend WebSocket connected")

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        print("🔌 Frontend WebSocket disconnected")
        frontend_socket = None

def get_frontend_socket():
    return frontend_socket
