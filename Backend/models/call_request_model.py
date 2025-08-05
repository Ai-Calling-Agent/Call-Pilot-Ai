from pydantic import BaseModel


class CallRequest(BaseModel):
    to: str  
    message: str  
