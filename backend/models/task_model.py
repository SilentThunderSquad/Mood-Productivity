"""models/task_model.py"""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = ""
    difficulty: Literal["Easy", "Medium", "Hard"] = "Medium"
    deadline: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[Literal["Easy", "Medium", "Hard"]] = None
    deadline: Optional[str] = None
    status: Optional[Literal["pending", "completed"]] = None


class TaskResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str]
    difficulty: str
    deadline: Optional[str]
    status: str
    created_at: Optional[datetime]
