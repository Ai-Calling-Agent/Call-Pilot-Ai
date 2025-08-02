import os
import assemblyai as aii
from dotenv import load_dotenv
load_dotenv()
aii.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

Twilio_SAMPLE_RATE = 8000 #hz

def on_open(session_opened:aii.RealtimeSessionOpened):
    print("SESSION ID:",session_opened.session_id)


def on_data(transcript:aii.RealtimeTranscript):
    if not transcript.text:
        print("No TEXT ON RealtimeTranscript")
        return
    
    if isinstance(transcript,aii.RealtimeFinalTranscript):
        print(transcript.text, '\r\n')  ## final transcript
    else:
        print(transcript.text, '\r')  ## partial transcript


def on_error(error:aii.RealtimeError):
    print("AN ERROR OCCURED ON ASSEMBLE-AI",error) 


def on_close():
    print("CLOSING SESSION")       
       

class TwilioTranscriber(aii.RealtimeTranscriber):
    def __init__(self):
        super().__init__(
            on_open=on_open,
            on_data=on_data,
            on_error=on_error,
            on_close=on_close,
            sample_rate=Twilio_SAMPLE_RATE,
            encoding=aii.AudioEncoding.pcm_mulaw,
        )