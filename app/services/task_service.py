from app.database import get_database
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate
from app.utils.helpers import convert_objectid_to_str
from bson import ObjectId
from typing import List, Optional
from datetime import datetime


class TaskService:
    COLLECTION_NAME = "tasks"

    @staticmethod
    async def create_task(task_data: TaskCreate) -> dict:
        """Create a new task"""
        db = get_database()
        collection = db[TaskService.COLLECTION_NAME]
        
        task_dict = task_data.model_dump()
        task_dict["intern_id"] = ObjectId(task_dict["intern_id"])
        # Convert date to datetime for MongoDB
        if "due_date" in task_dict and task_dict["due_date"]:
            from datetime import date as date_type
            if isinstance(task_dict["due_date"], date_type):
                task_dict["due_date"] = datetime.combine(task_dict["due_date"], datetime.min.time())
        task_dict["created_at"] = datetime.utcnow()
        
        result = await collection.insert_one(task_dict)
        task = await collection.find_one({"_id": result.inserted_id})
        task = convert_objectid_to_str(task)
        # Convert datetime back to date for response
        if task and "due_date" in task and isinstance(task["due_date"], datetime):
            task["due_date"] = task["due_date"].date()
        return Task(**task).model_dump(by_alias=True)

    @staticmethod
    async def get_task(task_id: str) -> Optional[dict]:
        """Get task by ID"""
        db = get_database()
        collection = db[TaskService.COLLECTION_NAME]
        
        if not ObjectId.is_valid(task_id):
            return None
            
        task = await collection.find_one({"_id": ObjectId(task_id)})
        if task:
            task = convert_objectid_to_str(task)
            # Ensure due_date is date type
            if task and "due_date" in task and isinstance(task["due_date"], datetime):
                task["due_date"] = task["due_date"].date()
            return Task(**task).model_dump(by_alias=True)
        return None

    @staticmethod
    async def get_all_tasks(intern_id: Optional[str] = None) -> List[dict]:
        """Get all tasks, optionally filtered by intern_id"""
        db = get_database()
        collection = db[TaskService.COLLECTION_NAME]
        
        query = {}
        if intern_id and ObjectId.is_valid(intern_id):
            query["intern_id"] = ObjectId(intern_id)
        
        cursor = collection.find(query)
        tasks = []
        async for doc in cursor:
            doc = convert_objectid_to_str(doc)
            # Ensure due_date is date type
            if doc and "due_date" in doc and isinstance(doc["due_date"], datetime):
                doc["due_date"] = doc["due_date"].date()
            tasks.append(Task(**doc).model_dump(by_alias=True))
        return tasks

    @staticmethod
    async def update_task(task_id: str, task_data: TaskUpdate) -> Optional[dict]:
        """Update task"""
        db = get_database()
        collection = db[TaskService.COLLECTION_NAME]
        
        if not ObjectId.is_valid(task_id):
            return None
        
        update_data = task_data.model_dump(exclude_unset=True)
        if not update_data:
            return await TaskService.get_task(task_id)
        
        # Convert date to datetime for MongoDB
        if "due_date" in update_data and update_data["due_date"]:
            from datetime import date as date_type
            if isinstance(update_data["due_date"], date_type):
                update_data["due_date"] = datetime.combine(update_data["due_date"], datetime.min.time())
        
        result = await collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            return await TaskService.get_task(task_id)
        return None

    @staticmethod
    async def complete_task(task_id: str) -> Optional[dict]:
        """Mark task as completed"""
        db = get_database()
        collection = db[TaskService.COLLECTION_NAME]
        
        if not ObjectId.is_valid(task_id):
            return None
        
        update_data = {
            "status": "completed",
            "completed_at": datetime.utcnow()
        }
        
        result = await collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": update_data}
        )
        
        if result.modified_count > 0:
            return await TaskService.get_task(task_id)
        return None

    @staticmethod
    async def delete_task(task_id: str) -> bool:
        """Delete task"""
        db = get_database()
        collection = db[TaskService.COLLECTION_NAME]
        
        if not ObjectId.is_valid(task_id):
            return False
        
        result = await collection.delete_one({"_id": ObjectId(task_id)})
        return result.deleted_count > 0

    @staticmethod
    async def get_intern_task_stats(intern_id: str) -> dict:
        """Get task statistics for an intern"""
        db = get_database()
        collection = db[TaskService.COLLECTION_NAME]
        
        if not ObjectId.is_valid(intern_id):
            return {"total": 0, "completed": 0, "pending": 0, "in_progress": 0}
        
        total = await collection.count_documents({"intern_id": ObjectId(intern_id)})
        completed = await collection.count_documents({
            "intern_id": ObjectId(intern_id),
            "status": "completed"
        })
        pending = await collection.count_documents({
            "intern_id": ObjectId(intern_id),
            "status": "pending"
        })
        in_progress = await collection.count_documents({
            "intern_id": ObjectId(intern_id),
            "status": "in_progress"
        })
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "in_progress": in_progress
        }


task_service = TaskService()
