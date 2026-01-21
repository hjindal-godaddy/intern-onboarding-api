from fastapi import APIRouter, HTTPException
from typing import List
from app.services import mentor_service
from app.schemas import MentorCreate, MentorUpdate, MentorResponse

router = APIRouter(prefix="/api/mentors", tags=["Mentors"])


@router.post("", response_model=MentorResponse, status_code=201)
async def create_mentor(mentor: MentorCreate):
    """Create a new mentor"""
    try:
        result = await mentor_service.create_mentor(mentor)
        if result:
            return MentorResponse(
                id=str(result["_id"]),
                name=result["name"],
                email=result["email"],
                department=result["department"],
                created_at=result["created_at"]
            )
        raise HTTPException(status_code=400, detail="Failed to create mentor")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[MentorResponse])
async def get_all_mentors():
    """Get all mentors"""
    try:
        mentors = await mentor_service.get_all_mentors()
        return [
            MentorResponse(
                id=str(mentor["_id"]),
                name=mentor["name"],
                email=mentor["email"],
                department=mentor["department"],
                created_at=mentor["created_at"]
            )
            for mentor in mentors
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{mentor_id}", response_model=MentorResponse)
async def get_mentor(mentor_id: str):
    """Get mentor by ID"""
    mentor = await mentor_service.get_mentor(mentor_id)
    if not mentor:
        raise HTTPException(status_code=404, detail="Mentor not found")
    
    return MentorResponse(
        id=str(mentor["_id"]),
        name=mentor["name"],
        email=mentor["email"],
        department=mentor["department"],
        created_at=mentor["created_at"]
    )


@router.put("/{mentor_id}", response_model=MentorResponse)
async def update_mentor(mentor_id: str, mentor: MentorUpdate):
    """Update mentor"""
    result = await mentor_service.update_mentor(mentor_id, mentor)
    if not result:
        raise HTTPException(status_code=404, detail="Mentor not found")
    
    return MentorResponse(
        id=str(result["_id"]),
        name=result["name"],
        email=result["email"],
        department=result["department"],
        created_at=result["created_at"]
    )


@router.delete("/{mentor_id}", status_code=204)
async def delete_mentor(mentor_id: str):
    """Delete mentor"""
    success = await mentor_service.delete_mentor(mentor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Mentor not found")
    return None
