"""Services for Fast api kafka."""
from functools import lru_cache

from aiokafka import AIOKafkaProducer
from fastapi import Depends

from broker.kafka import KafkaBroker
from db.kafka_db import get_kafka_producer


@lru_cache()
def get_kafka_service(
        kafka_producer: AIOKafkaProducer = Depends(get_kafka_producer),
) -> AIOKafkaProducer:
    """Для внедрения зависимостей."""
    return KafkaBroker(kafka_producer)
