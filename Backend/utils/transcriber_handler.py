import asyncio
import base64
import json
from llm.groq_llm import get_real_estate_response
debounce_task = None
llm_speaking = None

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
    global debounce_task, llm_speaking

    transcript = data["transcript"].strip()


   

    # Cancel the previous debounce if still pending
    if debounce_task and not debounce_task.done():
        debounce_task.cancel()

    # Debounce response with 2s delay
    debounce_task = asyncio.create_task(handle_llm_response_after_delay(transcript, frontend_socket))


async def handle_llm_response_after_delay(transcript, frontend_socket):
    global llm_speaking

    try:
        await asyncio.sleep(3)

        if llm_speaking:
            print("⏳ LLM is already speaking, skipping response to:", transcript)
            return

        print("📤 Final Transcript:", transcript)

        llm_speaking = True
        response_text = await get_real_estate_response(transcript)
        print("LLM" , response_text)

        if frontend_socket:
            await frontend_socket.send_json({
                "type": "final_transcript",
                "user": transcript,
                "llm_response": response_text,
            })

     
    except asyncio.CancelledError:
        print("🛑 LLM debounce task was cancelled (user spoke again)")
    finally:
        llm_speaking = False