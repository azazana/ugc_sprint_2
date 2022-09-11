"""Основной модуль для запуска fastapi."""

from http import HTTPStatus
from typing import Callable, Tuple
from uuid import uuid4

import aiokafka
import sentry_sdk
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse

from api.v1 import movies
from core.config import settings
from db import kafka_db

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=settings.traces_sample_rate,
    )

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)

app.include_router(movies.router, prefix="/api/v1/movies", tags=["movies"])


@app.on_event("startup")
async def startup() -> None:
    """Иницилиазация продьюсера кафки."""
    if kafka_db:
        kafka_db.kafka_producer = aiokafka.AIOKafkaProducer(
            bootstrap_servers=f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}",
        )


@app.on_event("shutdown")
async def shutdown() -> None:
    """Окончание работы продьюсера."""
    if kafka_db:
        await kafka_db.kafka_producer.stop()  # type: ignore


@app.middleware("http")
async def request_middleware(request: Request, call_next: Callable) -> ORJSONResponse:
    """Добавление requist id в заголовки."""
    id_header: Tuple[bytes, bytes] = "x-request-id".encode(), str(uuid4()).encode()
    request.headers.__dict__["_list"].append(id_header)
    try:
        response = await call_next(request)
    except Exception:
        response = ORJSONResponse(content={"success": False}, status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
    return response


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_config=None,
    )
