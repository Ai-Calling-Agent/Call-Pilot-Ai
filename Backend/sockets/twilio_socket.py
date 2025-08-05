import json
from fastapi import WebSocket, WebSocketDisconnect
from twilio_transcriber import TwilioTranscriber
from utils.transcriber_handler import handle_twilio_event, send_final_transcript

async def handle_twilio_socket(websocket: WebSocket, frontend_socket):
    await websocket.accept()
    print("🟢 Twilio WebSocket connected")

    transcriber = TwilioTranscriber(
        on_final_transcript=lambda data: send_final_transcript(frontend_socket, data),
        on_complete_turn=lambda data: None  # You can expand this
    )

    try:
        while True:
            message = await websocket.receive_text()
            data = json.loads(message)
            await handle_twilio_event(data, transcriber, frontend_socket)
    except WebSocketDisconnect:
        print("🔴 Twilio disconnected")
        await transcriber.terminate_session()
