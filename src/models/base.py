"""Модели для валидации данных из фаст апи."""

from typing import Any

import orjson
from pydantic import BaseModel


def orjson_dumps(v: Any, *, default: Any) -> Any:
    """Декодер."""
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class OrjsonModel(BaseModel):
    """Базовый класс для orjson-моделей."""

    class Config:
        """Настройки для текущего класса."""

        json_loads = orjson.loads
        json_dumbs = orjson_dumps


class MovieModel(OrjsonModel):
    """Класс для валидации данных из фаст апи."""

    topic: str
    id_user: str
    id_movie: str
    timestamp: str
    event: str

    class Config:
        """Настройки для текущего класса."""

        json_loads = orjson.loads
        json_dumbs = orjson_dumps


class Parameters(OrjsonModel):
    """Параметры для фастапи."""

    id_user: str
    id_movie: str
    timestamp: str
    event: str
