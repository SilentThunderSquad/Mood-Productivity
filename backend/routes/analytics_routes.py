"""routes/analytics_routes.py"""
from fastapi import APIRouter, Depends

from database import tasks_collection, moods_collection
from auth import get_current_user
from analytics_engine import calculate_productivity_score, analyze_moods, generate_weekly_report

router = APIRouter(prefix="/api", tags=["analytics"])


@router.get("/productivity-score")
async def productivity_score(current_user: dict = Depends(get_current_user)):
    tasks_col = tasks_collection()
    result = tasks_col.select("*").eq("user_id", current_user["sub"]).execute()
    return calculate_productivity_score(result.data or [])


@router.get("/mood-analytics")
async def mood_analytics(current_user: dict = Depends(get_current_user)):
    moods_col    = moods_collection()
    result = moods_col.select("*").eq("user_id", current_user["sub"]).order("timestamp", desc=True).limit(200).execute()
    return analyze_moods(result.data or [])


@router.get("/weekly-report")
async def weekly_report(current_user: dict = Depends(get_current_user)):
    tasks_col    = tasks_collection()
    moods_col    = moods_collection()
    
    tasks_res = tasks_col.select("*").eq("user_id", current_user["sub"]).execute()
    moods_res = moods_col.select("*").eq("user_id", current_user["sub"]).order("timestamp", desc=True).limit(200).execute()
    
    return generate_weekly_report(tasks_res.data or [], moods_res.data or [])
