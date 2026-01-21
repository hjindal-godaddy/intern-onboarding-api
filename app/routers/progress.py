from fastapi import APIRouter, HTTPException
from app.services import intern_service, task_service
from app.schemas import ProgressResponse, ProgressUpdate
from typing import Optional

router = APIRouter(prefix="/api/interns", tags=["Progress"])


@router.get("/{intern_id}/progress", response_model=ProgressResponse)
async def get_intern_progress(intern_id: str):
    """Get intern progress based on completed tasks"""
    # Verify intern exists
    intern = await intern_service.get_intern(intern_id)
    if not intern:
        raise HTTPException(status_code=404, detail="Intern not found")
    
    # Get task statistics
    stats = await task_service.get_intern_task_stats(intern_id)
    
    # Calculate completion percentage
    if stats["total"] == 0:
        completion_percentage = 0.0
    else:
        completion_percentage = (stats["completed"] / stats["total"]) * 100
    
    # Create progress response
    from datetime import datetime
    from bson import ObjectId
    
    return ProgressResponse(
        id=str(ObjectId()),
        intern_id=intern_id,
        completion_percentage=round(completion_percentage, 2),
        last_updated=datetime.utcnow()
    )


@router.post("/{intern_id}/progress/update", response_model=ProgressResponse)
async def update_intern_progress(intern_id: str, progress: ProgressUpdate):
    """Manually update intern progress (alternative to auto-calculation)"""
    # Verify intern exists
    intern = await intern_service.get_intern(intern_id)
    if not intern:
        raise HTTPException(status_code=404, detail="Intern not found")
    
    from datetime import datetime
    from bson import ObjectId
    
    return ProgressResponse(
        id=str(ObjectId()),
        intern_id=intern_id,
        completion_percentage=progress.completion_percentage,
        last_updated=datetime.utcnow()
    )
