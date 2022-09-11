"""CRUD на лайки."""
from typing import Any

from fastapi import APIRouter

from src.models.like import Like
from src.servises.crud import likes

router = APIRouter()


@router.get("/{user_id}", response_model=list[Like])
async def get_likes_list(
        user_id: str,
        limit: int = 10,
        offset: int = 0,
) -> Any:
    """
    Likes list.
    """
    return await likes.get_likes_list(user_id=user_id, limit=limit, offset=offset)


@router.post("/{user_id}/{film_id}", response_model=Like)
async def create_like(
        user_id: str,
        film_id: str,
) -> Any:
    """
    Create new like.
    """
    return await likes.create_like(user_id=user_id, film_id=film_id)


@router.get("/{user_id}/{film_id}", response_model=Like)
async def read_category(
        user_id: str,
        film_id: str,
) -> Any:
    """
    Get a like.
    """
    like = await likes.get_like(user_id=user_id, film_id=film_id)
    return like


@router.delete("/{user_id}/{film_id}", response_model=str)
async def delete_category(
        user_id: str,
        film_id: str,
) -> Any:
    """
    Delete like.
    """
    await likes.remove_like(user_id=user_id, film_id=film_id)
    return "DONE"
