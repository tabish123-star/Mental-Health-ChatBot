from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from chatbot import MentalHealthChatbot
from database import ChatDatabase

app = FastAPI(
    title="Mental Health Support Chatbot API",
    description="A supportive, non-diagnostic mental health chatbot built with FastAPI.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bot = MentalHealthChatbot()
db = ChatDatabase()


class ChatRequest(BaseModel):
    user_id: str = Field(default="anonymous", min_length=1, max_length=100)
    message: str = Field(..., min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    user_id: str
    message: str
    response: str
    mood: str
    crisis_detected: bool
    timestamp: str


class MoodRequest(BaseModel):
    user_id: str = Field(default="anonymous", min_length=1, max_length=100)
    mood: str = Field(..., min_length=1, max_length=30)


@app.get("/")
def home():
    return {
        "message": "Mental Health Support Chatbot API is running",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "mental-health-chatbot"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    message = request.message.strip()

    if not message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    result = bot.generate_response(message)

    db.save_chat(
        user_id=request.user_id,
        user_message=message,
        bot_response=result["response"],
        mood=result["mood"],
        crisis_detected=result["crisis_detected"],
    )

    return ChatResponse(
        user_id=request.user_id,
        message=message,
        response=result["response"],
        mood=result["mood"],
        crisis_detected=result["crisis_detected"],
        timestamp=datetime.utcnow().isoformat(),
    )


@app.post("/mood")
def save_mood(request: MoodRequest):
    allowed_moods = {
        "happy", "sad", "anxious", "angry",
        "stressed", "calm", "neutral", "tired"
    }

    mood = request.mood.lower().strip()

    if mood not in allowed_moods:
        raise HTTPException(
            status_code=400,
            detail=f"Mood must be one of: {', '.join(sorted(allowed_moods))}",
        )

    db.save_mood(request.user_id, mood)

    return {
        "message": "Mood saved successfully.",
        "user_id": request.user_id,
        "mood": mood,
    }


@app.get("/history/{user_id}")
def get_history(user_id: str, limit: int = 20):
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100.",
        )

    return {
        "user_id": user_id,
        "history": db.get_history(user_id, limit),
    }


@app.get("/moods/{user_id}")
def get_moods(user_id: str, limit: int = 30):
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 100.",
        )

    return {
        "user_id": user_id,
        "moods": db.get_moods(user_id, limit),
    }


@app.delete("/history/{user_id}")
def delete_history(user_id: str):
    db.delete_history(user_id)
    return {"message": "Chat history deleted.", "user_id": user_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
