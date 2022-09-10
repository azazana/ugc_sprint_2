"""Тестовая загрузка данных в ClickHouse."""

import time
from typing import Callable
from uuid import uuid4

from fake_data import fake_batch, fake_bookmark_event, fake_like_event, fake_review_event, fake_users_batch
from settings_research import settings

from .clickhouse import ClickhouseAdapter

adapter = ClickhouseAdapter(host=settings.CLICKHOUSE_HOST, user=settings.USER_CH, password=settings.PASSWORD_CH)
ITERATIONS_NUMBER = 10
USERS_IN_BATCH = 10
OPTIMAL_BATCH_SIZE = 1000
TEST_RECORDS_SIZE = 10000


def init_clickhouse(
        fields: dict[str, str], table: str,
) -> None:
    """Инициализация таблицы в ClickHouse."""
    adapter.create_db(settings.SHARD_DB, cluster=settings.CLICKHOUSE_CLUSTER)
    adapter.create_db(settings.REPLICA_DB, cluster=settings.CLICKHOUSE_CLUSTER)
    adapter.create_table_distributed(
        table_name=table,
        fields=fields,
        partition_by=None,
        order_by="user_id",
    )


def test_insert_step(
        faker: Callable,
        collection_name: str,
        batch_size: int,
        iterations: int = ITERATIONS_NUMBER,
) -> None:
    """Тестирование вставки."""
    statistics = []
    for _ in range(iterations):
        batch = fake_batch(faker, USERS_IN_BATCH, batch_size)
        start = time.time()
        step_data = []
        str_key = ""
        for value in batch:
            str_key = ", ".join(value.keys())
            step_data.append(tuple(value.values()))
        adapter.execute(f"""INSERT INTO {collection_name} ({str_key}) VALUES""", step_data)
        end = time.time()
        statistics.append(end - start)
    mean_batch = sum(statistics) / len(statistics)
    print(
        f"Statistics for {collection_name} batch_size={batch_size}: batch={mean_batch} sec, "
        f"item={mean_batch / batch_size} sec.",
    )


def test_insert(faker: Callable, collection_name: str) -> None:
    """Тестирование вставки с разным размером батча."""
    batch_sizes = [1, 10, 50, 100, 200, 500, 1000, 2000, 5000]
    for batch_size in batch_sizes:
        test_insert_step(faker, collection_name, batch_size)


def test_read_data(faker: Callable, collection_name: str, users_size: int) -> None:
    """Тестирование чтения."""
    statistics = []
    users = [str(uuid4()) for _ in range(users_size)]

    for _ in range(0, TEST_RECORDS_SIZE, OPTIMAL_BATCH_SIZE):
        batch = fake_users_batch(faker, users, batch_size=OPTIMAL_BATCH_SIZE)
        adapter.execute(f"""INSERT INTO {collection_name} (user_id) VALUES""", batch)

    for user in users:
        start = time.time()
        _ = list(adapter.execute(f"SELECT * FROM {collection_name} WHERE user_id = '{user}'"))
        statistics.append(time.time() - start)

    mean_batch = sum(statistics) / len(statistics)
    print(
        f"Statistics read for {collection_name} for ~{int(TEST_RECORDS_SIZE / users_size)} records: {mean_batch} sec",
    )


if __name__ == "__main__":
    # лайки
    init_clickhouse(fields={
        "user_id": "String",
        "film_id": "String",
        "type": "UInt32",
        "datetime": "DateTime",
    }, table=settings.COLLECTION_LIKE)
    # отзывы
    init_clickhouse(fields={
        "user_id": "String",
        "film_id": "String",
        "text": "String",
        "rating": "UInt32",
        "datetime": "DateTime",
    }, table=settings.COLLECTION_REVIEW)
    # закладки
    init_clickhouse(fields={
        "user_id": "String",
        "film_id": "String",
        "datetime": "DateTime",
    }, table=settings.COLLECTION_BOOKMARK)

    test_insert(fake_like_event, settings.COLLECTION_LIKE)
    test_insert(fake_review_event, settings.COLLECTION_REVIEW)
    test_insert(fake_bookmark_event, settings.COLLECTION_BOOKMARK)

    test_read_data(fake_like_event, settings.COLLECTION_LIKE, 20)
    test_read_data(fake_review_event, settings.COLLECTION_REVIEW, 20)
    test_read_data(fake_bookmark_event, settings.COLLECTION_BOOKMARK, 20)
