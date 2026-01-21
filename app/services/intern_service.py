from app.database import get_database
from app.models import Intern
from app.schemas import InternCreate, InternUpdate
from app.utils.helpers import convert_objectid_to_str
from bson import ObjectId
from typing import List, Optional
from datetime import datetime


class InternService:
    COLLECTION_NAME = "interns"

    @staticmethod
    async def create_intern(intern_data: InternCreate) -> dict:
        """Create a new intern"""
        db = get_database()
        collection = db[InternService.COLLECTION_NAME]
        
        intern_dict = intern_data.model_dump()
        # Convert date to datetime for MongoDB
        if "start_date" in intern_dict and intern_dict["start_date"]:
            from datetime import date as date_type
            if isinstance(intern_dict["start_date"], date_type):
                intern_dict["start_date"] = datetime.combine(intern_dict["start_date"], datetime.min.time())
        intern_dict["created_at"] = datetime.utcnow()
        intern_dict["updated_at"] = datetime.utcnow()
        
        result = await collection.insert_one(intern_dict)
        intern = await collection.find_one({"_id": result.inserted_id})
        intern = convert_objectid_to_str(intern)
        # Convert datetime back to date for response
        if intern and "start_date" in intern and isinstance(intern["start_date"], datetime):
            intern["start_date"] = intern["start_date"].date()
        return Intern(**intern).model_dump(by_alias=True)

    @staticmethod
    async def get_intern(intern_id: str) -> Optional[dict]:
        """Get intern by ID"""
        db = get_database()
        collection = db[InternService.COLLECTION_NAME]
        
        if not ObjectId.is_valid(intern_id):
            return None
            
        intern = await collection.find_one({"_id": ObjectId(intern_id)})
        if intern:
            intern = convert_objectid_to_str(intern)
            return Intern(**intern).model_dump(by_alias=True)
        return None

    @staticmethod
    async def get_all_interns() -> List[dict]:
        """Get all interns"""
        db = get_database()
        collection = db[InternService.COLLECTION_NAME]
        
        cursor = collection.find({})
        interns = []
        async for doc in cursor:
            doc = convert_objectid_to_str(doc)
            # Ensure start_date is date type
            if doc and "start_date" in doc and isinstance(doc["start_date"], datetime):
                doc["start_date"] = doc["start_date"].date()
            interns.append(Intern(**doc).model_dump(by_alias=True))
        return interns

    @staticmethod
    async def update_intern(intern_id: str, intern_data: InternUpdate) -> Optional[dict]:
        """Update intern"""
        db = get_database()
        collection = db[InternService.COLLECTION_NAME]
        
        if not ObjectId.is_valid(intern_id):
            return None
        
        update_data = intern_data.model_dump(exclude_unset=True)
        if not update_data:
            return await InternService.get_intern(intern_id)
        
        update_data["updated_at"] = datetime.utcnow()
        
        # Handle mentor_id conversion if provided
        if "mentor_id" in update_data and update_data["mentor_id"]:
            if ObjectId.is_valid(update_data["mentor_id"]):
                update_data["mentor_id"] = ObjectId(update_data["mentor_id"])
            else:
                update_data["mentor_id"] = None
        
        result = await collection.update_one(
            {"_id": ObjectId(intern_id)},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            return await InternService.get_intern(intern_id)
        return None

    @staticmethod
    async def delete_intern(intern_id: str) -> bool:
        """Delete intern"""
        db = get_database()
        collection = db[InternService.COLLECTION_NAME]
        
        if not ObjectId.is_valid(intern_id):
            return False
        
        result = await collection.delete_one({"_id": ObjectId(intern_id)})
        return result.deleted_count > 0

    @staticmethod
    async def assign_mentor(intern_id: str, mentor_id: str) -> Optional[dict]:
        """Assign a mentor to an intern"""
        if not ObjectId.is_valid(intern_id) or not ObjectId.is_valid(mentor_id):
            return None
        
        update_data = InternUpdate(mentor_id=mentor_id)
        return await InternService.update_intern(intern_id, update_data)


intern_service = InternService()
