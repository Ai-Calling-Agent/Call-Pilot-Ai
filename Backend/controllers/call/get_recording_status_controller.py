
from fastapi import Request

async def recording_status(request: Request):
    data = await request.form()
    print("✅ Recording complete")
    print("📞 Call SID:", data.get("CallSid"))
    print("🎧 Recording URL:", data.get("RecordingUrl"))
    print("⏱ Duration (sec):", data.get("RecordingDuration"))
    return "OK"