"""Интерфейс брокера сообщений."""
from abc import ABC, abstractmethod


class EventBroker(ABC):
    """Абстрактный класс для брокера сообщений."""

    @abstractmethod
    async def send_data_to_broker(self, key: str, value: str, topic: str) -> str:
        """Отправка сообщений."""
        pass
