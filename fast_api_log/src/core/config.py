"""Config for fast api kafka."""

import logging
from logging import config as logging_config

from pydantic import BaseSettings

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)
logger = logging.getLogger()


class Settings(BaseSettings):
    """Настройки проекта."""

    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = "movies"
    KAFKA_HOST: str = "broker"
    KAFKA_PORT: str = "29092"


settings = Settings()
logger.info(settings.dict())
