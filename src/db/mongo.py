"""Mongo DB adapter."""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorCursor

from src.core.config import settings


class Mongo:
    """Mongo DB adapter."""

    def __init__(self) -> None:
        """Init."""
        self.client = AsyncIOMotorClient(settings.MONGO_HOST, settings.MONGO_PORT)
        self.db = self.client[settings.MONGO_DB]

    def _get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        """Get collection."""
        return self.db[collection_name]

    async def find(
            self,
            collection_name: str,
            condition: dict,
            limit: int = settings.DEFAULT_LIMIT,
            offset: int = settings.DEFAULT_OFFSET,
    ) -> AsyncIOMotorCursor:
        """Read data from mongoDB."""
        collection = self._get_collection(collection_name)
        return collection.find(condition).skip(offset).limit(limit)

    async def insert(
            self,
            collection_name: str,
            data: dict,
    ) -> None:
        """Insert data in mongoDB."""
        collection = self._get_collection(collection_name)
        await collection.insert_one(data)

    async def find_one(
            self,
            collection_name: str,
            condition: dict,
    ) -> dict:
        """Read item from mongoDB."""
        collection = self._get_collection(collection_name)
        return await collection.find_one(condition)

    async def delete(
            self,
            collection_name: str,
            condition: dict,
    ) -> None:
        """Delete from mongoDB."""
        collection = self._get_collection(collection_name)
        await collection.delete_many(condition)
