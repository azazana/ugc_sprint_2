"""Ручки для ETL."""

from http import HTTPStatus

from broker.kafka import KafkaBroker
from core.config import logger
from fastapi import APIRouter, Depends, HTTPException
from models.base import MovieModel, Parameters
from servises.views_movies import get_kafka_service
import os
router = APIRouter()


@router.post(
    "/",
    summary="Статус просмотра фильма",
    response_description="Сообщение для кафки о статусе просмотра фильма",
)
async def put_film_to_kafka(
        param: Parameters = Depends(),
        kafka_service: KafkaBroker = Depends(get_kafka_service)) -> str:
    """
    Отправка сообщений о статусе просмотра фильма.

    - **id_user**: id пользователя
    - **id_movie**: id фильма
    - **value**: Значение метки о просмотре фильма
    - **event**: Тип события
    **return**: ошибка или сообщение о успешном успехе.
    """
    try:
        movie_model = MovieModel(topic="movie", **param.dict())
        return await kafka_service.send_msg(**movie_model.dict())
    except Exception as exception:
        logger.exception(exception)
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)


@router.get("/sentry-debug",
            summary="Тестирование sentry",
            response_description="Используется для тестирования sentry",
            )
async def trigger_error():
    """
    Отправка сообщений о статусе просмотра фильма.
    """
    division_by_zero = 1 / 0
