from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from routes.call.call_route import router as call_router

# ✅ Step 1: Create FastAPI app for normal HTTP routes
app = FastAPI()
app.include_router(call_router)
app.include_router
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
