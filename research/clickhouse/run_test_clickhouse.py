"""Тестовая загрузка данных в ClickHouse."""

import logging
import time
from random import randint
from uuid import uuid4

from settings_research import settings

from clickhouse import ClickhouseAdapter

# logging.basicConfig(filename="research/clickhouse_log.log", encoding="utf-8", level=logging.INFO,
#                     format="%(asctime)s - %(message)s")
adapter = ClickhouseAdapter(host=settings.CLICKHOUSE_HOST, user=settings.USER_CH, password=settings.PASSWORD_CH)


def init_clickhouse(
        fields: dict[str, str],
) -> None:
    """Инициализация таблицы в ClickHouse."""
    # logging.info("Initialize ClickHouse started.")
    adapter.create_db(settings.SHARD_DB, cluster=settings.CLICKHOUSE_CLUSTER)
    adapter.create_db(settings.REPLICA_DB, cluster=settings.CLICKHOUSE_CLUSTER)
    adapter.create_table_distributed(
        table_name=settings.TABLE_TEST,
        fields=fields,
        partition_by=None,
        order_by="user_id",
    )
    # logging.info("Initialize ClickHouse finished.")


def fake_data(
        table_name: str,
        size: int = 300000,
        batch_size: int = 200,
        count_step: int = 100000,
) -> list:
    """Генерирует фейковые данные и проводит тестирование загрузки."""
    print(f"Run size={size}, batch_size={batch_size}, count_step={count_step}")
    generated = 0
    times = []
    local_times = []
    count_step_ind = 1

    while generated < size:
        step_data = []
        for _ in range(batch_size):
            user_id = randint(0, 1000000)
            movie_id = str(uuid4())
            viewed_frame = randint(0, 200)
            step_data.append(f"{user_id}, '{movie_id}', {viewed_frame}")
            generated += 1

        data = " UNION ALL SELECT ".join(step_data)
        start = time.time()
        adapter.execute(f"""INSERT INTO {table_name} (user_id, movie_id, viewed_frame) SELECT {data}""")
        local_times.append(time.time() - start)

        if generated >= count_step_ind * count_step:
            sum_time = sum(local_times)
            local_times = []
            count_step_ind += 1
            print(f"INSERT of {generated}/{size} done. Last step time: {sum_time}.")
            times.append(sum_time)

    return times


if __name__ == "__main__":
    init_clickhouse(fields={
        "user_id": "UInt32",
        "movie_id": "String",
        "viewed_frame": "UInt32",
    })

    batches = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
    batches_info = {}
    for batch in batches:
        batches_info[batch] = fake_data(
            settings.TABLE_TEST,
            size=2000000,
            batch_size=batch,
        )

    for batch_size, data in batches_info.items():
        print(batch_size, sum(data) / len(data))
