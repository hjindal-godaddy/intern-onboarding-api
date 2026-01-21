from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services import task_service
from app.schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate):
    """Create a new task"""
    try:
        result = await task_service.create_task(task)
        if result:
            return TaskResponse(
                id=str(result["_id"]),
                intern_id=str(result["intern_id"]),
                title=result["title"],
                description=result.get("description"),
                status=result["status"],
                due_date=result.get("due_date"),
                completed_at=result.get("completed_at"),
                created_at=result["created_at"]
            )
        raise HTTPException(status_code=400, detail="Failed to create task")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[TaskResponse])
async def get_all_tasks(intern_id: Optional[str] = Query(None, description="Filter by intern ID")):
    """Get all tasks, optionally filtered by intern_id"""
    try:
        tasks = await task_service.get_all_tasks(intern_id)
        return [
            TaskResponse(
                id=str(task["_id"]),
                intern_id=str(task["intern_id"]),
                title=task["title"],
                description=task.get("description"),
                status=task["status"],
                due_date=task.get("due_date"),
                completed_at=task.get("completed_at"),
                created_at=task["created_at"]
            )
            for task in tasks
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get task by ID"""
    task = await task_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskResponse(
        id=str(task["_id"]),
        intern_id=str(task["intern_id"]),
        title=task["title"],
        description=task.get("description"),
        status=task["status"],
        due_date=task.get("due_date"),
        completed_at=task.get("completed_at"),
        created_at=task["created_at"]
    )


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: str, task: TaskUpdate):
    """Update task"""
    result = await task_service.update_task(task_id, task)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskResponse(
        id=str(result["_id"]),
        intern_id=str(result["intern_id"]),
        title=result["title"],
        description=result.get("description"),
        status=result["status"],
        due_date=result.get("due_date"),
        completed_at=result.get("completed_at"),
        created_at=result["created_at"]
    )


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(task_id: str):
    """Mark task as completed"""
    result = await task_service.complete_task(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskResponse(
        id=str(result["_id"]),
        intern_id=str(result["intern_id"]),
        title=result["title"],
        description=result.get("description"),
        status=result["status"],
        due_date=result.get("due_date"),
        completed_at=result.get("completed_at"),
        created_at=result["created_at"]
    )


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: str):
    """Delete task"""
    success = await task_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None
