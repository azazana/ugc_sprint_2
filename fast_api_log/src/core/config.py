"""Config for fast api kafka."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки проекта."""

    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = "movies"
    KAFKA_HOST: str = "broker"
    KAFKA_PORT: str = "29092"


settings = Settings()
