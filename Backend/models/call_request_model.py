from pydantic import BaseModel


class CallRequest(BaseModel):
    to: str  # E.g., "+91xxxxxxxxxx"
    message: str  # Custom voice message