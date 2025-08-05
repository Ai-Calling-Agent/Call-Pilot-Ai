import asyncio
import base64
from llm.groq_llm import get_real_estate_response
from textToSpeeach.audio_utils import convert_mp3_to_mulaw
from textToSpeeach.elevenlabs_tts import text_to_speech_elevenlabs
from twilio_transcriber import TwilioTranscriber

debounce_task = None
llm_speaking = False

async def handle_twilio_socket(twilio_ws, frontend_ws):
    async def on_final_transcript(data):
        transcript = data["transcript"].strip()
        print("📥 User said:", transcript)

        global debounce_task
        if debounce_task and not debounce_task.done():
            debounce_task.cancel()

        # Debounced reply
        debounce_task = asyncio.create_task(
            handle_llm_response_after_delay(transcript, frontend_ws, twilio_ws)
        )

    transcriber = TwilioTranscriber(
        on_final_transcript=on_final_transcript,
        frontend_websocket=frontend_ws
    )

    await transcriber.connect()

    try:
        while True:
            data = await twilio_ws.receive_json()

            match data["event"]:
                case "connected":
                    await transcriber.connect()
                    print("✅ Twilio connected")

                case "start":
                    print("▶️ Call started")

                case "media":
                    audio_b64 = data["media"]["payload"]
                    audio_bytes = base64.b64decode(audio_b64)
                    await transcriber.stream_audio(audio_bytes)

                case "stop":
                    print("⏹️ Call ended")
                    await transcriber.terminate_session()
                    break

    except Exception as e:
        print("❌ Error in Twilio WebSocket:", e)
        await twilio_ws.close()


async def handle_llm_response_after_delay(transcript, frontend_ws, twilio_ws):
    global llm_speaking
    try:
        await asyncio.sleep(2)

        if llm_speaking:
            print("⏳ LLM still speaking, skipping...")
            return

        llm_speaking = True
        response_text = await get_real_estate_response(transcript)
        print("🤖 LLM:", response_text)

        if frontend_ws:
            await frontend_ws.send_json({
                "type": "final_transcript",
                "user": transcript,
                "llm_response": response_text
            })

        # Generate audio
        mp3_audio = text_to_speech_elevenlabs(response_text)
        mulaw_audio = convert_mp3_to_mulaw(mp3_audio)

        # Send to Twilio in 160-byte chunks (20ms each)
        chunk_size = 160
        for i in range(0, len(mulaw_audio), chunk_size):
            chunk = mulaw_audio[i:i+chunk_size]
            payload = base64.b64encode(chunk).decode("utf-8")
            await twilio_ws.send_json({
                "event": "media",
                "media": { "payload": payload }
            })
            await asyncio.sleep(0.02)  # 20ms

    except asyncio.CancelledError:
        print("🛑 Debounced task cancelled")
    finally:
        llm_speaking = False
