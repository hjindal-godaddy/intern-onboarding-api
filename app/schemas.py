from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime, date
from bson import ObjectId


# PyObjectId removed - using str directly for ObjectId fields


# Intern Schemas
class InternCreate(BaseModel):
    name: str
    email: EmailStr
    start_date: date
    status: Optional[str] = "active"


class InternUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    start_date: Optional[date] = None
    status: Optional[str] = None
    mentor_id: Optional[str] = None


class InternResponse(BaseModel):
    id: str
    name: str
    email: str
    start_date: date
    status: str
    mentor_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Task Schemas
class TaskCreate(BaseModel):
    intern_id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = "pending"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[date] = None


class TaskResponse(BaseModel):
    id: str
    intern_id: str
    title: str
    description: Optional[str] = None
    status: str
    due_date: Optional[date] = None
    completed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Mentor Schemas
class MentorCreate(BaseModel):
    name: str
    email: EmailStr
    department: str


class MentorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None


class MentorResponse(BaseModel):
    id: str
    name: str
    email: str
    department: str
    created_at: datetime

    class Config:
        from_attributes = True


# Progress Schemas
class ProgressResponse(BaseModel):
    id: str
    intern_id: str
    completion_percentage: float
    last_updated: datetime

    class Config:
        from_attributes = True


class ProgressUpdate(BaseModel):
    completion_percentage: float = Field(ge=0, le=100)


# OpenAI Schemas
class WelcomeMessageRequest(BaseModel):
    custom_message: Optional[str] = None


class WelcomeMessageResponse(BaseModel):
    message: str


class DocumentSummarizeRequest(BaseModel):
    document_text: str
    max_length: Optional[int] = 200


class DocumentSummarizeResponse(BaseModel):
    summary: str
