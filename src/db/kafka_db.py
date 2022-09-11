"""Для внедрения зависимостей."""
from typing import Optional

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

kafka_producer: Optional[AIOKafkaProducer] = None
kafka_consumer: Optional[AIOKafkaConsumer] = None


async def get_kafka_producer() -> AIOKafkaProducer:
    """Для внедрения зависимостей."""
    return kafka_producer


async def get_kafka_consumer() -> AIOKafkaConsumer:
    """Для внедрения зависимостей."""
    return kafka_consumer
