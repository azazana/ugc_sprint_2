"""Брокер сообщений кафка."""
import json
import logging
from uuid import uuid4

from aiokafka import AIOKafkaProducer
from api.v1.logging_setup import setup_root_logger
from broker.base import EventBroker

log_filename = "logs/fastapi-elk-stack.log"
# Get logger for module
LOGGER = logging.getLogger(__name__)
setup_root_logger(log_filename,LOGGER)


class KafkaBroker(EventBroker):
    """Кафка брокер сообщений."""

    def __init__(self, producer: AIOKafkaProducer) -> None:
        """Инициализация."""
        self.producer = producer

    async def send_data_to_broker(self, key: str, value: str, topic: str) -> str:
        """Send data to kafka."""
        await self.producer.start()
        producer = self.producer

        try:
            await producer.send_and_wait(
                topic=topic,
                value=bytes(value, encoding="utf8"),
                key=bytes(key, encoding="utf8"),
            )
            LOGGER.info("data has excepted by kafka")
            return "data has excepted by kafka"
        except Exception:
            LOGGER.error("Ошибка в отправке данных в кафку")
            return "Ошибка в отправке данных в кафку"
        # finally:
        #     await producer.stop()

    async def send_msg(self, topic: str, id_user: str, id_movie: str, timestamp: str, event: str) -> str:
        """Send message to kafka."""
        key = f"{id_user}.{uuid4()}"
        value = {
            "user_id": id_user,
            "film_id": id_movie,
            "event": event,
            "timestamp": timestamp,
        }
        message = await self.send_data_to_broker(topic=topic, key=key, value=json.dumps(value))
        return message
