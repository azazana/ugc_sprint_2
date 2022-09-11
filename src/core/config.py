"""Config for fast api kafka."""

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Настройки проекта."""

    # Название проекта. Используется в Swagger-документации
    PROJECT_NAME: str = "movies"
    KAFKA_HOST: str = "broker"
    KAFKA_PORT: str = "29092"
    SENTRY_DSN = "https://ca4101b36d3f43f6919a7e79890ff60a@o1384570.ingest.sentry.io/6703096"
    traces_sample_rate = 0.0


settings = Settings()
