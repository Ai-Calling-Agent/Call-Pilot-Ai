from fastapi import HTTPException
from models.call_request_model import CallRequest
from twilio.rest import Client
from constant.api_keys import account_sid,auth_token,twilio_number,verified_number



client = Client(account_sid, auth_token)

def make_voice_call(payload: CallRequest):
    try:
        call = client.calls.create(
            twiml=f'<Response><Say>{payload.message}</Say></Response>',
            to=verified_number,
            from_=twilio_number
        )
        return {"message": "Call initiated", "sid": call.sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))