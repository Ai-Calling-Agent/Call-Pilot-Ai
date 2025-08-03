import base64
from twilio_transcriber import TwilioTranscriber 
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
async def websocket_connection(websocket: WebSocket):
    global frontend_socket
    await websocket.accept()
    print("🟢 Twilio connected")
    async def send_partial_transcript(data):
        if frontend_socket:
            try:
                await frontend_socket.send_json({
                    "type": "partial_transcript",
                    "text": data["transcript"],
                    "confidence": data["confidence"],
                    "segments": data["segments"],
                })
                print("📤 Sent complete user turn to frontend")
            except Exception as e:
                print(f"❌ Failed to send partial transcript: {e}")

    async def send_final_transcript(data):
        # Forward to frontend socket if available
        if frontend_socket:
            try:
                await frontend_socket.send_json({
                    "type": "final_transcript",
                    "text": data["transcript"],
                    "confidence": data["confidence"]
                })
                print("✅ Sent transcript to frontend")
            except Exception as e:
                print(f"❌ Failed to send to frontend: {e}")
        else:
            print("⚠️ No frontend socket connected")

    transcriber = TwilioTranscriber(
    on_final_transcript=send_final_transcript,
    on_complete_turn=send_partial_transcript
)

    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)

            match data["event"]:
                case "connected":
                    await transcriber.connect()
                    print("Twilio Connected!!")

                case "start":
                    print("Twilio started!!!")

                case "media":
                    payload_b64 = data["media"]["payload"]
                    payload_mulaw = base64.b64decode(payload_b64)
                    await transcriber.stream_audio(payload_mulaw)

                case "stop":
                    print("Twilio Stopped")
                    await transcriber.terminate_session()

    except WebSocketDisconnect:
        print("❌ Twilio disconnected")
        await transcriber.terminate_session()









frontend_socket = None
@app.websocket("/ws/client")
async def websocket_endpoint(websocket: WebSocket):
    global frontend_socket
    await websocket.accept()
    print("🟢 Frontend WebSocket connected")
    
    frontend_socket = websocket  # Save the frontend connection

    try:
        while True:
            await websocket.receive_text()  # keep connection alive
    except WebSocketDisconnect:
        print("🔌 Frontend WebSocket disconnected")
        frontend_socket = None
