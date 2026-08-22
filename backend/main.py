from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from backend.groq_service import generate_response


app = FastAPI(
    title="Harsh Ingle AI Portfolio API",
    description="AI-powered portfolio assistant",
    version="1.0.0"
)


# Allow frontend to communicate with backend

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "Harsh Ingle AI Portfolio API is running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    answer = generate_response(request.message)

    return {
        "response": answer
    }