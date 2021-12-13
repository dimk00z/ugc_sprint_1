from kafka import KafkaConsumer
from etl.config import (
    KAFKA_HOST,
    KAFKA_GROUP_ID,
    KAFKA_TOPIC
)


class ETLKafkaConsumer:

    def __init__(self):
        self.host = KAFKA_HOST
        self.topic = KAFKA_TOPIC
        self.group_id = KAFKA_GROUP_ID

    def get_consumer(self):
        return KafkaConsumer(
            self.topic,
            bootstrap_servers=self.host
        )
