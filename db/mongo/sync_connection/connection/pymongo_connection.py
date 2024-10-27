import pymongo
from pymongo.errors import ConnectionFailure
import logging
from config.enviroment.env_config import settings

class SyncMongoDBClient:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            try:
                cls._client = pymongo.MongoClient(settings.MONGO_DB_URL)
                # Check the connection
                cls._client.admin.command('ping')
                logging.info("Connected to MongoDB")
            except ConnectionFailure as e:
                logging.error(f"MongoDB connection failed: {e}")
                raise e
        return cls._client

    @classmethod
    def get_database(cls):
        client = cls.get_client()
        return client[settings.MONGO_DB_NAME]

def get_sync_connection():
    return SyncMongoDBClient.get_database()
