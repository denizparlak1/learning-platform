from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure
import logging
from config.enviroment.env_config import settings


# Singleton MongoDB Client
class MongoDBClient:
    _client: AsyncIOMotorClient = None

    @classmethod
    async def get_client(cls) -> AsyncIOMotorClient:
        if cls._client is None:
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
        return client[settings.MONGO_DB_NAME]

# Dependency for FastAPI routes
async def get_database() -> AsyncIOMotorClient:
    return await MongoDBClient.get_database()
