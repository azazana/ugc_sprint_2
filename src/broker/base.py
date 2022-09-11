"""Интерфейс брокера сообщений."""
from abc import ABC, abstractmethod
from typing import Any


class EventBroker(ABC):
    """Абстрактный класс для брокера сообщений."""

    @abstractmethod
    def send_data_to_broker(self, *kwargs) -> Any:
        """Отправка сообщений."""
        pass
