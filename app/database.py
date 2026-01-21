from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from typing import Optional


class Database:
    client: Optional[AsyncIOMotorClient] = None


database = Database()


async def connect_to_mongo():
    """Create database connection"""
    database.client = AsyncIOMotorClient(settings.mongodb_url)
    # Test the connection
    await database.client.admin.command('ping')
    print(f"Connected to MongoDB: {settings.database_name}")


async def close_mongo_connection():
    """Close database connection"""
    if database.client:
        database.client.close()
        print("Disconnected from MongoDB")


def get_database():
    """Get database instance"""
    return database.client[settings.database_name]
