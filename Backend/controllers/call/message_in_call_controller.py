from fastapi import APIRouter, Request, Response

from constant.generate_url import generate_Socket_url

url = generate_Socket_url("ws")

async def message_in_call(req:Request):

    twiml = f"""
    <Response>
        <Start>
            <Stream url="{url}" />  
        </Start>
        <Say voice="alice" language="en-US">Hello from call AI</Say>
        <Pause length="30"/>
    </Response>
    """
    return Response(content=twiml.strip(), media_type="text/xml")
