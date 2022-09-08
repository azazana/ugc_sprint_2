"""Генерация фейковых данных для исслдеования."""
from random import choice, randint
from typing import Callable
from uuid import uuid4

from faker import Faker

LIKE = 1
DISLIKE = 0
START_DATE = "-30d"
END_DATE = "now"
MIN_RATING = 1
MAX_RATING = 10
fake = Faker()


def fake_like_event(user_id: str = None, film_id: str = None) -> dict:
    """Генерация события like."""
    return {
        "user_id": user_id if user_id else str(uuid4()),
        "film_id": film_id if film_id else str(uuid4()),
        "type": choice([LIKE, DISLIKE]),
        "datetime": fake.date_time_between(start_date=START_DATE, end_date=END_DATE),
    }


def fake_review_event(user_id: str = None, film_id: str = None) -> dict:
    """Генерация события review."""
    return {
        "user_id": user_id if user_id else str(uuid4()),
        "film_id": film_id if film_id else str(uuid4()),
        "text": fake.text(),
        "rating": randint(MIN_RATING, MAX_RATING),
        "datetime": fake.date_time_between(start_date=START_DATE, end_date=END_DATE),
    }


def fake_bookmark_event(user_id: str = None, film_id: str = None) -> dict:
    """Генерация события bookmark."""
    return {
        "user_id": user_id if user_id else str(uuid4()),
        "film_id": film_id if film_id else str(uuid4()),
        "datetime": fake.date_time_between(start_date=START_DATE, end_date=END_DATE),
    }


def fake_batch(event_faker: Callable, user_size: int, batch_size: int) -> list[dict]:
    """Генерация батча событий."""
    users = [str(uuid4()) for _ in range(user_size)]
    return [event_faker(user_id=choice(users)) for _ in range(batch_size)]


def fake_users_batch(event_faker: Callable, users: list, batch_size: int) -> list[dict]:
    """Генерация батча событий с фиксированными юзерами."""
    return [event_faker(user_id=choice(users)) for _ in range(batch_size)]
