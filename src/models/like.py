"""Pydantic модели для CRUD лайков."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Like(BaseModel):
    """Модель лайков."""

    user_id: str
    film_id: str
    dt: Optional[datetime] = None
