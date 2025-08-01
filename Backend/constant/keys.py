import os
from dotenv import load_dotenv
load_dotenv()

account_sid = os.getenv("TWILLO_ACCOUNT_SID")
auth_token = os.getenv("TWILLO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")
verified_number = os.getenv("TWILIO_VERIFIED_NUMBER")
base_url = os.getenv("BASE_URL")