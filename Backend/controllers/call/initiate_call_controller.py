import html
from constant.keys import base_url
from fastapi import HTTPException
from models.call_request_model import CallRequest
from twilio.rest import Client
from constant.keys import account_sid, auth_token, twilio_number, verified_number

client = Client(account_sid, auth_token)

async def make_voice_call(payload: CallRequest):
    try:
        call = client.calls.create(
            url=base_url+"/voice",
            to=verified_number,
            from_=twilio_number,
            record=True,
            recording_status_callback=base_url+"/recording-status",
            recording_status_callback_method="POST"
        )
        return {
            "message": "Call initiated",
            "sid": call.sid,
            "status": call.status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


