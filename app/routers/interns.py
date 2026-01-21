from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.services.intern_service import intern_service
from app.services.mentor_service import mentor_service
from app.services.openai_service import openai_service
from app.schemas import (
    InternCreate, 
    InternUpdate, 
    InternResponse,
    WelcomeMessageRequest,
    WelcomeMessageResponse
)

router = APIRouter(prefix="/api/interns", tags=["Interns"])


@router.post("", response_model=InternResponse, status_code=201)
async def create_intern(intern: InternCreate):
    """Create a new intern"""
    try:
        result = await intern_service.create_intern(intern)
        if result:
            return InternResponse(
                id=str(result["_id"]),
                name=result["name"],
                email=result["email"],
                start_date=result["start_date"],
                status=result["status"],
                mentor_id=str(result["mentor_id"]) if result.get("mentor_id") else None,
                created_at=result["created_at"],
                updated_at=result["updated_at"]
            )
        raise HTTPException(status_code=400, detail="Failed to create intern")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[InternResponse])
async def get_all_interns():
    """Get all interns"""
    try:
        interns = await intern_service.get_all_interns()
        return [
            InternResponse(
                id=str(intern["_id"]),
                name=intern["name"],
                email=intern["email"],
                start_date=intern["start_date"],
                status=intern["status"],
                mentor_id=str(intern["mentor_id"]) if intern.get("mentor_id") else None,
                created_at=intern["created_at"],
                updated_at=intern["updated_at"]
            )
            for intern in interns
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{intern_id}", response_model=InternResponse)
async def get_intern(intern_id: str):
    """Get intern by ID"""
    intern = await intern_service.get_intern(intern_id)
    if not intern:
        raise HTTPException(status_code=404, detail="Intern not found")
    
    return InternResponse(
        id=str(intern["_id"]),
        name=intern["name"],
        email=intern["email"],
        start_date=intern["start_date"],
        status=intern["status"],
        mentor_id=str(intern["mentor_id"]) if intern.get("mentor_id") else None,
        created_at=intern["created_at"],
        updated_at=intern["updated_at"]
    )


@router.put("/{intern_id}", response_model=InternResponse)
async def update_intern(intern_id: str, intern: InternUpdate):
    """Update intern"""
    result = await intern_service.update_intern(intern_id, intern)
    if not result:
        raise HTTPException(status_code=404, detail="Intern not found")
    
    return InternResponse(
        id=str(result["_id"]),
        name=result["name"],
        email=result["email"],
        start_date=result["start_date"],
        status=result["status"],
        mentor_id=str(result["mentor_id"]) if result.get("mentor_id") else None,
        created_at=result["created_at"],
        updated_at=result["updated_at"]
    )


@router.delete("/{intern_id}", status_code=204)
async def delete_intern(intern_id: str):
    """Delete intern"""
    success = await intern_service.delete_intern(intern_id)
    if not success:
        raise HTTPException(status_code=404, detail="Intern not found")
    return None


@router.post("/{intern_id}/welcome-message", response_model=WelcomeMessageResponse)
async def generate_welcome_message(
    intern_id: str,
    request: Optional[WelcomeMessageRequest] = None
):
    """Generate a personalized welcome message for an intern"""
    intern = await intern_service.get_intern(intern_id)
    if not intern:
        raise HTTPException(status_code=404, detail="Intern not found")
    
    mentor_name = None
    if intern.get("mentor_id"):
        mentor = await mentor_service.get_mentor(str(intern["mentor_id"]))
        if mentor:
            mentor_name = mentor["name"]
    
    custom_message = request.custom_message if request else None
    
    message = await openai_service.generate_welcome_message(
        intern_name=intern["name"],
        intern_email=intern["email"],
        start_date=str(intern["start_date"]),
        mentor_name=mentor_name,
        custom_message=custom_message
    )
    
    return WelcomeMessageResponse(message=message)


@router.put("/{intern_id}/assign-mentor/{mentor_id}", response_model=InternResponse)
async def assign_mentor(intern_id: str, mentor_id: str):
    """Assign a mentor to an intern"""
    # Verify intern exists
    intern = await intern_service.get_intern(intern_id)
    if not intern:
        raise HTTPException(status_code=404, detail="Intern not found")
    
    # Verify mentor exists
    mentor = await mentor_service.get_mentor(mentor_id)
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    
    result = await intern_service.assign_mentor(intern_id, mentor_id)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to assign mentor")
    
    return InternResponse(
        id=str(result["_id"]),
        name=result["name"],
        email=result["email"],
        start_date=result["start_date"],
        status=result["status"],
        mentor_id=str(result["mentor_id"]) if result.get("mentor_id") else None,
        created_at=result["created_at"],
        updated_at=result["updated_at"]
    )
