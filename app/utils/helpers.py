from bson import ObjectId
from datetime import datetime, date
from typing import Any, Dict


def convert_objectid_to_str(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert ObjectId fields to strings and datetime to date for Pydantic models"""
    if not doc:
        return doc
    
    # Convert _id
    if "_id" in doc and isinstance(doc["_id"], ObjectId):
        doc["_id"] = str(doc["_id"])
    
    # Convert other ObjectId fields (like mentor_id, intern_id)
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
        # Convert datetime to date for date fields
        elif isinstance(value, datetime) and key in ["start_date", "due_date"]:
            doc[key] = value.date()
    
    return doc
