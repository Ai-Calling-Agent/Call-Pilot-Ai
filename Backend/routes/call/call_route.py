from controllers.call.call_controller import make_voice_call
from fastapi import APIRouter

from models.call_request_model import CallRequest

router = APIRouter()

@router.post("/call")
async def startCall(payload:CallRequest):
    return await make_voice_call(payload)        
