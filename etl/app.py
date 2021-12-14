import json
import logging

from clickhouse_driver import Client
from clickhouse_driver.errors import Error
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from modules.ch import ETLClickhouseDriver
from modules.kafka import ETLKafkaConsumer

from settings.config import get_settings
from settings.logging import LOGGING


def transform(data):
    payload = {}
    try:
        for key, val in data.items():
            if isinstance(val, dict):
                payload = payload | val
            else:
                payload[key] = val
    except Exception as transform_ex:
        logging.error("Error while transforming data: {0}".format(transform_ex))
    return payload


def load(client: Client, data: dict = {}):
    try:
        table = get_settings().ch_settings.table
        client.execute(f"INSERT INTO {table} VALUES", data, types_check=True)
        return True
    except KeyError as ch_err:
        logging.error("Error while loading data into Clickhouse: {0}".format(ch_err))


def run(kafka_consumer: KafkaConsumer, ch_driver: Client, batch_size: int = 100):
    while True:
        try:
            batch = []
            while len(batch) < batch_size:
                for msg in kafka_consumer:
                    value = json.loads(msg.value)
                    payload = transform(value)
                    batch.append(payload)
            res = ch_driver.load(batch)
            if not res:
                continue

        except KafkaError as kafka_error:
            logging.error("Got Kafka error: {0}".format(kafka_error))

        except Error as ch_error:
            logging.error("Got ClickHouse error: {0}".format(ch_error))


if __name__ == "__main__":
    settings = get_settings()
    consumer = ETLKafkaConsumer(**settings.kafka_settings.dict())
    ch_driver = ETLClickhouseDriver(settings.ch_settings.host)
    run(consumer, ch_driver, batch_size=settings.app.batch_size)
