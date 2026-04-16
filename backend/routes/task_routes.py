"""routes/task_routes.py"""
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone

from database import tasks_collection
from auth import get_current_user
from models.task_model import TaskCreate, TaskUpdate

router = APIRouter(prefix="/api", tags=["tasks"])

@router.post("/task")
async def create_task(data: TaskCreate, current_user: dict = Depends(get_current_user)):
    tasks = tasks_collection()
    doc = {
        "user_id":     current_user["sub"],
        "title":       data.title,
        "description": data.description or "",
        "difficulty":  data.difficulty,
        "deadline":    data.deadline,
        "status":      "pending",
        "created_at":  datetime.now(timezone.utc).isoformat(),
    }
    result = tasks.insert(doc).execute()
    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create task")
    return {"message": "Task created", "task": result.data[0]}

@router.get("/tasks")
async def get_tasks(current_user: dict = Depends(get_current_user)):
    tasks = tasks_collection()
    result = tasks.select("*").eq("user_id", current_user["sub"]).execute()
    return {"tasks": result.data}

@router.put("/task/{task_id}")
async def update_task(task_id: str, data: TaskUpdate, current_user: dict = Depends(get_current_user)):
    tasks = tasks_collection()
    update_fields = {k: v for k, v in data.dict().items() if v is not None}
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = tasks.update(update_fields).eq("id", task_id).eq("user_id", current_user["sub"]).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task updated"}

@router.delete("/task/{task_id}")
async def delete_task(task_id: str, current_user: dict = Depends(get_current_user)):
    tasks = tasks_collection()
    result = tasks.delete().eq("id", task_id).eq("user_id", current_user["sub"]).execute()
    return {"message": "Task deleted"}

@router.put("/task/complete/{task_id}")
async def complete_task(task_id: str, current_user: dict = Depends(get_current_user)):
    tasks = tasks_collection()
    result = tasks.update({
        "status": "completed", 
        "completed_at": datetime.now(timezone.utc).isoformat()
    }).eq("id", task_id).eq("user_id", current_user["sub"]).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task marked complete"}
