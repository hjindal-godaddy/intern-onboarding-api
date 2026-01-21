from app.database import get_database
from app.models import Mentor
from app.schemas import MentorCreate, MentorUpdate
from app.utils.helpers import convert_objectid_to_str
from bson import ObjectId
from typing import List, Optional
from datetime import datetime


class MentorService:
    COLLECTION_NAME = "mentors"

    @staticmethod
    async def create_mentor(mentor_data: MentorCreate) -> dict:
        """Create a new mentor"""
        db = get_database()
        collection = db[MentorService.COLLECTION_NAME]
        
        mentor_dict = mentor_data.model_dump()
        mentor_dict["created_at"] = datetime.utcnow()
        
        result = await collection.insert_one(mentor_dict)
        mentor = await collection.find_one({"_id": result.inserted_id})
        mentor = convert_objectid_to_str(mentor)
        return Mentor(**mentor).model_dump(by_alias=True)

    @staticmethod
    async def get_mentor(mentor_id: str) -> Optional[dict]:
        """Get mentor by ID"""
        db = get_database()
        collection = db[MentorService.COLLECTION_NAME]
        
        if not ObjectId.is_valid(mentor_id):
            return None
            
        mentor = await collection.find_one({"_id": ObjectId(mentor_id)})
        if mentor:
            mentor = convert_objectid_to_str(mentor)
            return Mentor(**mentor).model_dump(by_alias=True)
        return None

    @staticmethod
    async def get_all_mentors() -> List[dict]:
        """Get all mentors"""
        db = get_database()
        collection = db[MentorService.COLLECTION_NAME]
        
        cursor = collection.find({})
        mentors = []
        async for doc in cursor:
            doc = convert_objectid_to_str(doc)
            mentors.append(Mentor(**doc).model_dump(by_alias=True))
        return mentors

    @staticmethod
    async def update_mentor(mentor_id: str, mentor_data: MentorUpdate) -> Optional[dict]:
        """Update mentor"""
        db = get_database()
        collection = db[MentorService.COLLECTION_NAME]
        
        if not ObjectId.is_valid(mentor_id):
            return None
        
        update_data = mentor_data.model_dump(exclude_unset=True)
        if not update_data:
            return await MentorService.get_mentor(mentor_id)
        
        result = await collection.update_one(
            {"_id": ObjectId(mentor_id)},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            return await MentorService.get_mentor(mentor_id)
        return None

    @staticmethod
    async def delete_mentor(mentor_id: str) -> bool:
        """Delete mentor"""
        db = get_database()
        collection = db[MentorService.COLLECTION_NAME]
        
        if not ObjectId.is_valid(mentor_id):
            return False
        
        result = await collection.delete_one({"_id": ObjectId(mentor_id)})
        return result.deleted_count > 0


mentor_service = MentorService()
