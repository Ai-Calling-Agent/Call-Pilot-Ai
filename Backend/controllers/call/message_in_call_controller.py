
from fastapi import Response
async def voice():
    twiml = """
    <Response>
        <Say voice="alice">You are now connected. This call will be recorded.</Say>
        <Pause length="1"/>
        <Record maxLength="300" timeout="5" transcribe="false" />
        <Hangup/>
    </Response>
    """
    return Response(content=twiml, media_type="application/xml")
