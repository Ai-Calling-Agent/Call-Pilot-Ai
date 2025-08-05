from constant.generate_url import generate_url
from constant.keys import base_url
from fastapi import HTTPException
from constant.keys import account_sid, auth_token, twilio_number, verified_number
from twilio.rest import Client
from models.call_request_model import CallRequest

client = Client(account_sid, auth_token)
url = generate_url("outgoingcallmessage")


async def make_outgoing_call(payload: CallRequest):
    try:
        call = client.calls.create(
            url=url,
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