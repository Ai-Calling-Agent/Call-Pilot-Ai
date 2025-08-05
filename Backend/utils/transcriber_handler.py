import base64
import json
from llm.groq_llm import get_real_estate_response

async def handle_twilio_event(data, transcriber, frontend_socket):
    match data["event"]:
        case "connected":
            await transcriber.connect()
            print("✅ Twilio connected")

        case "start":
            print("▶️ Call started")

        case "media":
            payload_b64 = data["media"]["payload"]
            payload_mulaw = base64.b64decode(payload_b64)
            await transcriber.stream_audio(payload_mulaw)

        case "stop":
            print("⏹️ Call ended")
            await transcriber.terminate_session()

async def send_final_transcript(frontend_socket, data):
    print("📤 Final Transcript:", data["transcript"])
    response_text = await get_real_estate_response(data["transcript"])
    
    if frontend_socket:
        await frontend_socket.send_json({
            "type": "final_transcript",
            "user": data["transcript"],
            "llm_response": response_text,
        })
