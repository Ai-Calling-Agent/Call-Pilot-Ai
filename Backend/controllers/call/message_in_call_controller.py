from fastapi import APIRouter, Request, Response


async def message_in_call(req:Request):
    host = req.headers.get("host") 
    stream_url = f"wss://{host}/ws"

    twiml = f"""
    <Response>
        <Start>
            <Stream url="{stream_url}" />  
        </Start>
        <Say voice="alice" language="en-US">Hello from call AI</Say>
        <Pause length="30"/>
    </Response>
    """
    return Response(content=twiml.strip(), media_type="text/xml")
