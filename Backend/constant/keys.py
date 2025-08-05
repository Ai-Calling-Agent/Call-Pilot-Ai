import os
from dotenv import load_dotenv
load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")
verified_number = os.getenv("TWILIO_VERIFIED_NUMBER")
base_url = os.getenv("BASE_URL")
base_Socket_url = os.getenv("BASE_Socket_URL")
