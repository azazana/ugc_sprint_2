"""Адаптер для ClickHouse."""
from datetime import datetime
from typing import Any, Optional

import backoff
from clickhouse_driver import Client, errors

from settings_research import settings


class ClickhouseAdapter:
    """Адаптер для ClickHouse."""

    def __init__(self, host: str, user: str, password: str) -> None:
        """Инициализация."""
        self.client = Client(
            host=host,
            user=user,
            password=password,
        )

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(errors.ServerException, errors.Error, errors.NetworkError, errors.SocketTimeoutError),
        max_time=settings.DB_BACKOFF_MAX_TIME,
        max_tries=settings.DB_BACKOFF_MAX_TRIES,
        raise_on_giveup=False,
    )
    def execute(self, command: str) -> Optional[Any]:
        """Исполнение запроса в ClickHouse."""
        try:
            return self.client.execute(command)
        except errors.ServerException as exception:
            if exception.code != 57:
                raise exception

    def create_db(self, database: str, cluster: Optional[str] = None) -> None:
        """Создание БД в ClickHouse."""
        command = f"CREATE DATABASE IF NOT EXISTS {database}"
        if cluster:
            command += f" ON CLUSTER {cluster}"
        self.execute(command=command)

    def create_table(
            self,
            table_name: str,
            fields: dict[str, str],
            engine: str,
            cluster: Optional[str] = None,
            partition_by: Optional[str] = None,
            order_by: Optional[str] = None,
    ) -> None:
        """Создание таблицы в ClickHouse."""
        fields_str = ", ".join([f"{key} {value}" for key, value in fields.items()])
        command = f"CREATE TABLE IF NOT EXISTS {table_name}"

        if cluster:
            command += f" ON CLUSTER {cluster}"

        command += f" ({fields_str}) ENGINE = {engine}"

        if partition_by:
            command += f" PARTITION BY {partition_by}"
        if order_by:
            command += f" ORDER BY {order_by}"

        self.execute(command=command)

    @staticmethod
    def _distributed_table_name(table_name: str) -> str:
        """Генирация названия для распределённой таблицы в ClickHouse."""
        return f"default.{table_name}"

    def create_table_distributed(
            self,
            table_name: str,
            fields: dict[str, str],
            partition_by: Optional[str] = None,
            order_by: Optional[str] = None,
    ) -> None:
        """Создание распределённой таблицы в ClickHouse."""
        self.create_table(
            table_name=table_name,
            fields=fields,
            cluster=settings.CLICKHOUSE_CLUSTER,
            engine=f"ReplicatedMergeTree('/clickhouse/tables/{{shard}}/{table_name}', '{{replica}}')",
            partition_by=partition_by,
            order_by=order_by,
        )
        self.create_table(
            table_name=self._distributed_table_name(table_name=table_name),
            fields=fields,
            cluster=settings.CLICKHOUSE_CLUSTER,
            engine=f"Distributed({settings.CLICKHOUSE_CLUSTER}, '', {table_name}, rand())",
        )

    @staticmethod
    def _generate_insert_item(item: Any) -> str:
        """Генерация строки item для insert-команды."""
        if isinstance(item, int) or isinstance(item, float):
            return str(item)
        if isinstance(item, datetime):
            return f"toDateTime('{item.strftime('%Y-%m-%d %H:%M:%S')}')"
        return f"'{item}'"

    def insert(self, table_name: str, data: list[dict[str, str]], distributed: bool = True) -> None:
        """Вставка данных в ClickHouse."""
        if not data:
            return

        keys = list(data[0].keys())
        values = []
        for item in data:
            values_item_str = ", ".join([self._generate_insert_item(item[key]) for key in keys])
            values.append(f"({values_item_str})")
        keys_str = ", ".join(keys)
        values_str = ", ".join(values)

        if distributed:
            table_name = self._distributed_table_name(table_name=table_name)

        self.execute(f"INSERT INTO {table_name} ({keys_str}) VALUES {values_str}")

    def select(self, table_name: str, fields: list[str] = None, distributed: bool = True) -> list:
        """Зароса данных из ClickHouse."""
        if fields:
            fields_str = ", ".join(fields)
        else:
            fields_str = "*"

        if distributed:
            table_name = self._distributed_table_name(table_name=table_name)

        return self.execute(f"SELECT {fields_str} FROM {table_name}")
