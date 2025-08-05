from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from sockets.twilio_socket import handle_twilio_socket
from sockets.client_socket import handle_client_socket, get_frontend_socket
from routes.call.call_route import router as call_router

app = FastAPI()
app.include_router(call_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Real Estate AI Assistant is live 🚀"}

@app.websocket("/ws")
async def twilio_ws(websocket: WebSocket):
    await handle_twilio_socket(websocket, get_frontend_socket())

@app.websocket("/ws/client")
async def client_ws(websocket: WebSocket):
    await handle_client_socket(websocket)
