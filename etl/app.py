import backoff
import logging
import json

from kafka import KafkaConsumer
from clickhouse_driver import Client

from kafka.errors import KafkaError
from clickhouse_driver.errors import Error

from modules.kafka import ETLKafkaConsumer
from modules.ch import ETLClickhouseDriver
from config import BATCH_SIZE, CH_TABLE


def transform(data):
    payload = {}
    try:
        for key, val in data.items():
            if isinstance(val, dict):
                payload = payload | val
            else:
                payload[key] = val
    except Exception as transform_ex:
        logging.error('Error while transforming data: {0}'.format(transform_ex))
    return payload


def load(client: Client, data: dict = {}):
    try:
        client.execute(f'INSERT INTO {CH_TABLE} VALUES', data, types_check=True)
        return True
    except KeyError as ch_err:
        logging.error('Error while loading data into Clickhouse: {0}'.format(ch_err))


def run(kafka_consumer: KafkaConsumer, ch_driver: Client):
    while True:
        try:
            batch = []
            while len(batch) < BATCH_SIZE:
                for msg in kafka_consumer:
                    value = json.loads(msg.value)
                    payload = transform(value)
                    batch.append(payload)
            res = ch_driver.load(batch)
            if not res:
                continue

        except KafkaError as kafka_error:
            logging.error('Got Kafka error: {0}'.format(kafka_error))

        except Error as ch_error:
            logging.error('Got ClickHouse error: {0}'.format(ch_error))


if __name__ == '__main__':
    consumer = ETLKafkaConsumer()
    ch_driver = ETLClickhouseDriver()
    run(consumer, ch_driver)
