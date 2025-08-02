import html

from fastapi import HTTPException
from constant.keys import account_sid, auth_token, twilio_number, verified_number
from twilio.rest import Client
from models.call_request_model import CallRequest

client = Client(account_sid, auth_token)

async def make_outgoing_call(payload: CallRequest):
    try:
        call = client.calls.create(
            url="https://0c9393b458f1.ngrok-free.app/outgoingcallmessage",
            to=verified_number,
            from_=twilio_number
        )
        return {
            "message": "Call initiated",
            "sid": call.sid,
            "status": call.status
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))