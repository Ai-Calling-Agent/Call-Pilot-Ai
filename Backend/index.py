import base64
import json
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from routes.call.call_route import router as call_router

app = FastAPI()
app.include_router(call_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def test():
    return Response(content="Hi")



# Sockets
@app.websocket("/ws")
async def websocket_connection(websocket:WebSocket):
    await websocket.accept()
    print("New Connection Initiated")
    try:
        while True: 
            message = await websocket.receive_text()
            parsed = json.loads(message)
            event = parsed.get("event")
            if event == "start":
                print("🔊 Stream started:", parsed.get("streamSid"))

            elif event == "media":
                # media.payload is base64-encoded audio (you need to decode + process for STT)
                print("🎧 Media received (base64 audio):", parsed["media"]["payload"][:30], "...")

            elif event == "stop":
                print("🛑 Stream ended")
                break
            
    except WebSocketDisconnect:
        print("❌ Client disconnected")


