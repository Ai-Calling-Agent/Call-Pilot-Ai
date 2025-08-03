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
    await websocket.accept()
    print("New Connection Initiated")
    transcriber = TwilioTranscriber()
    
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
                    print("Transcriber closed!!")
                    
    except WebSocketDisconnect:
        print("❌ Client disconnected")
        if transcriber.websocket and transcriber.websocket.close_code is None:
            await transcriber.terminate_session()
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        if transcriber.websocket and transcriber.websocket.close_code is None:
            await transcriber.terminate_session()