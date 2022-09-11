"""CRUD на лайки."""
from datetime import datetime
from http import HTTPStatus
from typing import Optional

from fastapi import HTTPException

from src.core.config import settings
from src.db.mongo import Mongo
from src.models.like import Like

mongo = Mongo()


async def get_likes_list(
        user_id: str,
        limit: int = settings.DEFAULT_LIMIT,
        offset: int = settings.DEFAULT_OFFSET,
) -> list[Like]:
    """Get likes list."""
    data = await mongo.find(settings.MONGO_COLLECTION_LIKE, {"user_id": user_id}, limit=limit, offset=offset)
    return [Like(**item) async for item in data]


async def get_like(user_id: str, film_id: str) -> Optional[Like]:
    """Get like."""
    data = await mongo.find_one(settings.MONGO_COLLECTION_LIKE, {"user_id": user_id, "film_id": film_id})
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
    return Like(**data)


async def create_like(user_id: str, film_id: str) -> Like:
    """Create like."""
    data = await mongo.find_one(settings.MONGO_COLLECTION_LIKE, {"user_id": user_id, "film_id": film_id})
    if data:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
    data = Like(user_id=user_id, film_id=film_id, dt=datetime.now())
    await mongo.insert(settings.MONGO_COLLECTION_LIKE, data.dict())
    return data


async def remove_like(user_id: str, film_id: str) -> None:
    """Remove like."""
    data = await mongo.find_one(settings.MONGO_COLLECTION_LIKE, {"user_id": user_id, "film_id": film_id})
    if not data:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)

    await mongo.delete(settings.MONGO_COLLECTION_LIKE, {"user_id": user_id, "film_id": film_id})
