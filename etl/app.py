import json
import logging

from clickhouse_driver.errors import Error
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from models.event import EventForUGS
from modules.ch import ETLClickhouseDriver
from modules.kafka import ETLKafkaConsumer

from settings.config import get_settings
from settings.logging import LOGGING


def transform(data):
    try:
        payload = EventForUGS(**data).dict()
        payload = payload | payload["payload"]
        payload.pop("payload")
    except Exception as transform_ex:
        logging.error("Error while transforming data: {0}".format(transform_ex))
    return payload or {}


def run(
    kafka_consumer: KafkaConsumer, ch_driver: ETLClickhouseDriver, batch_size: int = 100
):
    ch_driver.init_ch_database()
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
    consumer = ETLKafkaConsumer(**settings.kafka_settings.dict()).get_consumer()
    ch_driver = ETLClickhouseDriver(settings.ch_settings.host)
    run(consumer, ch_driver, batch_size=settings.app.batch_size)
