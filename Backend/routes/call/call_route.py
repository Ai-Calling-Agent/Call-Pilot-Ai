from fastapi import APIRouter, Request

from controllers.call.initiate_call_controller import make_outgoing_call
from controllers.call.message_in_call_controller import message_in_call
from models.call_request_model import CallRequest

router = APIRouter()


@router.post("/outgoingcallmessage")
async def generate_message(req:Request):
    return await message_in_call(req)


@router.post("/call")
async def make_call(payload:CallRequest):
    return await make_outgoing_call(payload)