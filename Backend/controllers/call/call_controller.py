import html
from fastapi import HTTPException
from models.call_request_model import CallRequest
from twilio.rest import Client
from constant.api_keys import account_sid, auth_token, twilio_number, verified_number

client = Client(account_sid, auth_token)

async def make_voice_call(payload: CallRequest):
    try:
        safe_message = html.escape(payload.message)
        twiml = f"""
                <Response>
                <Pause length="1"/>
                <Say voice="alice" language="en-US">{safe_message}</Say>
                </Response>
                """
        call = client.calls.create(
            twiml=twiml,
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


