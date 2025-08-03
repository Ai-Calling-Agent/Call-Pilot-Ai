import base64
import os

from groq import Groq
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


groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))  # Ensure GROQ_API_KEY is in your .env

# Sockets
@app.websocket("/ws")
async def websocket_connection(websocket: WebSocket):
    global frontend_socket
    await websocket.accept()
    print("🟢 Twilio connected")

    async def send_complete_turn_and_call_groq(data):
        transcript_text = data.get("transcript", "")

        # Send to frontend as complete user turn
        if frontend_socket:
            try:
                await frontend_socket.send_json({
                    "type": "complete_turn",
                    "text": transcript_text,
                    "segments": data.get("segments", []),
                    "confidence": data.get("confidence", 0)
                })
                print("📤 Sent complete user turn to frontend")
            except Exception as e:
                print(f"❌ Failed to send complete user turn: {e}")

        # Call Groq here only for completed turn
        try:
            groq_response = groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You're a helpful sales assistant that responds to customer calls about solar energy systems. "
                            "You sell 3 types of systems:\n"
                            "1. 3.2kW - suitable for small homes with basic appliances\n"
                            "2. 4.5kW - good for mid-size homes with 1 AC and kitchen appliances\n"
                            "3. 8.3kW - best for large homes or commercial needs, runs multiple ACs\n"
                            "Based on what the user says, provide clear and informative replies about these systems."
                        )
                    },
                    {"role": "user", "content": transcript_text},
                ]
            )
            reply = groq_response.choices[0].message.content
            print(f"🤖 Groq Response: {reply}")
        except Exception as e:
            print(f"❌ Error generating Groq response: {e}")
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

    async def send_final_transcript(data: dict):
        transcript_text = data.get("transcript", "")

        if frontend_socket:
            try:
                await frontend_socket.send_json({
                    "type": "final_transcript",
                    "text": transcript_text,
                    "confidence": data.get("confidence", 0)
                })
                print("✅ Sent transcript to frontend")
            except Exception as e:
                print(f"❌ Failed to send to frontend: {e}")
        else:
            print("⚠️ No frontend socket connected")

    # 👇 Generate response from Groq and log it
        try:
            groq_response = groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You're a helpful sales assistant that responds to customer calls about solar energy systems. "
                            "You sell 3 types of systems:\n"
                            "1. 3.2kW - suitable for small homes with basic appliances\n"
                            "2. 4.5kW - good for mid-size homes with 1 AC and kitchen appliances\n"
                            "3. 8.3kW - best for large homes or commercial needs, runs multiple ACs\n"
                            "Based on what the user says, provide clear and informative replies about these systems."
                        )
                    },
                    {"role": "user", "content": transcript_text},
                ]
            )
            reply = groq_response.choices[0].message.content
            print(f"🤖 Groq Response: {reply}")
        except Exception as e:
            print(f"❌ Error generating Groq response: {e}")



    transcriber = TwilioTranscriber(
    on_final_transcript=send_final_transcript,
    on_complete_turn=send_complete_turn_and_call_groq
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
