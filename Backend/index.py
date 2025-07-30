from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# ✅ Step 1: Create FastAPI app for normal HTTP routes
fastapi_app = FastAPI()

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Step 3: Define REST API routes on fastapi_app

@fastapi_app.get("/")
async def test():
    return {"message": "Hello medic-man"}
