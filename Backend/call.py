import os
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

account_sid = os.getenv("TWILLO_ACCOUNT_SID")
auth_token = os.getenv("TWILLO_AUTH_TOKEN")

client = Client(account_sid, auth_token)

call = client.calls.create(
    to="+919974598215",         # Your Indian number (must be verified)
    from_="+19785888517",         # Twilio US number you just "bought"
    url="http://demo.twilio.com/docs/voice.xml"  # Twilio-hosted voice message
)

print("Call SID:", call.sid)
