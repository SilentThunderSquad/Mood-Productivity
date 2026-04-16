"""routes/mood_routes.py — Q&A based mood assessment (replaces face detection)"""
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from pydantic import BaseModel
from typing import List, Dict

from database import moods_collection, tasks_collection
from auth import get_current_user
from mood_quiz_engine import derive_mood, get_questions, get_scores_for_answer
from recommendation_engine import recommend_tasks, get_focus_duration

router = APIRouter(prefix="/api", tags=["mood"])


class QuizAnswer(BaseModel):
    question_id: str
    value: str


class QuizSubmission(BaseModel):
    answers: List[QuizAnswer]


@router.get("/mood-questions")
async def mood_questions():
    """Return the list of check-in questions to display on the frontend."""
    return {"questions": get_questions()}


@router.post("/assess-mood")
async def assess_mood(data: QuizSubmission, current_user: dict = Depends(get_current_user)):
    """
    Accept quiz answers, derive mood, save to DB, return recommendations.
    """
    if len(data.answers) < 3:
        raise HTTPException(status_code=400, detail="Please answer at least 3 questions.")

    # Enrich answers with scores
    enriched = []
    for ans in data.answers:
        scores = get_scores_for_answer(ans.question_id, ans.value)
        enriched.append({
            "question_id": ans.question_id,
            "value":       ans.value,
            "scores":      scores,
        })

    result = derive_mood(enriched)

    # Persist mood record
    moods = moods_collection()
    mood_doc = {
        "user_id":       current_user["sub"],
        "detected_mood": result["mood"],
        "emotion":       result["mood"],   # kept same field for analytics compat
        "confidence":    85.0,
        "method":        "quiz",
        "scores":        result["scores"],
        "answers":       enriched,
        "timestamp":     datetime.now(timezone.utc).isoformat(),
    }
    moods.insert(mood_doc).execute()

    # Fetch pending tasks for recommendations
    tasks_col  = tasks_collection()
    tasks_res = tasks_col.select("*").eq("user_id", current_user["sub"]).eq("status", "pending").execute()
    user_tasks = tasks_res.data if tasks_res.data else []

    recs = recommend_tasks(result["mood"], user_tasks)

    return {
        **result,
        "recommendations": recs["recommended"],
        "urgent_tasks":    recs["urgent"],
        "focus_duration":  get_focus_duration(result["mood"]),
    }


@router.get("/mood-history")
async def mood_history(current_user: dict = Depends(get_current_user)):
    moods   = moods_collection()
    records = moods.select("*").eq("user_id", current_user["sub"]).order("timestamp", desc=True).limit(50).execute()
    return {"moods": records.data if records.data else []}
