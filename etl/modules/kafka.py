import backoff
from kafka import KafkaConsumer
from kafka.errors import KafkaError


class ETLKafkaConsumer:
    def __init__(self, host: str, topic: str, group_id: str):
        self.host = host
        self.topic = topic
        self.group_id = group_id

    @backoff.on_exception(backoff.expo, KafkaError)
    def get_consumer(self):
        return KafkaConsumer(
            self.topic, bootstrap_servers=self.host, group_id=self.group_id
        )
