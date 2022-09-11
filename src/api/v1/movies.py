"""Ручки для ETL."""

import logging
import random
from http import HTTPStatus
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Request

from api.v1.logging_setup import setup_root_logger
from broker.kafka import KafkaBroker
from models.base import MovieModel, Parameters
from servises.views_movies import get_kafka_service

log_filename = "logs/fastapi-elk-stack.log"
LOGGER = logging.getLogger(__name__)
setup_root_logger(log_filename, LOGGER)
# Get logger for module

LOGGER.info("---Starting App---")
router = APIRouter()


class RequestIdFilter(logging.Filter):
    """Добавление requist_id в заголовки сообщений."""

    def __init__(self, request: Optional[Request] = None) -> None:
        super().__init__()
        self.request = request

    def filter(self, record: Any) -> bool:
        """Фильтрация."""
        if self.request:
            record.request_id = self.request.headers.get("x-request-id")
        return True


@router.get(
    "/",
    summary="Тестирование логирования",
    response_description="Тестирование логирования данных",
)
async def index(request: Request) -> str:
    """
     Для тестирования log.
     """
    result = random.randint(1, 50)
    LOGGER.addFilter(RequestIdFilter(request))
    LOGGER.info(f"Пользователю досталось число {result}")
    return f"Ваше число {result}!"


@router.post(
    "/film",
    summary="Статус просмотра фильма",
    response_description="Сообщение для кафки о статусе просмотра фильма",
)
async def put_film_to_kafka(
        request: Request,
        param: Parameters = Depends(),
        kafka_service: KafkaBroker = Depends(get_kafka_service),
) -> str:
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
    except Exception:
        LOGGER.addFilter(RequestIdFilter(request))
        LOGGER.error("Ошибка в отправке данных в кафку")
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND)


@router.get(
    "/sentry-debug",
    summary="Тестирование sentry",
    response_description="Используется для тестирования sentry",
)
async def trigger_error(request: Request) -> None:
    """
    Для тестирования sentry.
    """
    _ = 1 / 0
