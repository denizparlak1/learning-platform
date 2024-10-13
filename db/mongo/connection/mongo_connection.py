from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
from fastapi import Depends
import logging
from pydantic_settings import BaseSettings

# Config class for database settings
class Settings(BaseSettings):
    MONGO_DB_URL: str
    MONGO_DB_NAME: str

    class Config:
        env_file = ".env"

# Singleton MongoDB Client
class MongoDBClient:
    _client: AsyncIOMotorClient = None

    @classmethod
    async def get_client(cls) -> AsyncIOMotorClient:
        if cls._client is None:
            settings = Settings()
            try:
                cls._client = AsyncIOMotorClient(settings.MONGO_DB_URL)
                # Check the connection
                await cls._client.admin.command('ping')
                logging.info("Connected to MongoDB")
            except ConnectionFailure as e:
                logging.error(f"MongoDB connection failed: {e}")
                raise e
        return cls._client

    @classmethod
    async def get_database(cls):
        client = await cls.get_client()
        settings = Settings()
        return client[settings.MONGO_DB_NAME]

# Dependency for FastAPI routes
async def get_database() -> AsyncIOMotorClient:
    return await MongoDBClient.get_database()
