"""models/mood_model.py"""
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime


class MoodDetectRequest(BaseModel):
    image: str  # base64-encoded image


class MoodResponse(BaseModel):
    emotion: str
    mood: str
    confidence: float
    all_emotions: Dict[str, float]
    description: str
    color: str
    icon: str
    success: bool
    timestamp: Optional[datetime] = None
