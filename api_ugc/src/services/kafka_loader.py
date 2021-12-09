import json
import logging
from random import randint

from kafka import KafkaProducer
from kafka.errors import KafkaError
from models.request import RequestForUGS
from utils.back_off import backoff, backoff_hdlr

from core.settings import get_settings

logger = logging.getLogger(__name__)


class KafkaLoader:
    @staticmethod
    @backoff.on_exception(
        backoff.expo, (Exception,), on_backoff=backoff_hdlr, max_tries=10
    )
    def get_producer(
        host: str = "127.0.0.1", port: int = 9092, retries_number: int = 5
    ) -> KafkaProducer:
        return KafkaProducer(
            bootstrap_servers=[f"{host}:{port}"],
            key_serializer=str.encode,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            retries=retries_number,
        )

    def __init__(self) -> None:
        self.host = get_settings().kafka_settings.host
        self.port = get_settings().kafka_settings.port
        self.retries_number = get_settings().kafka_settings.retries_number
        self.producer = KafkaLoader.get_producer(
            host=self.host, port=self.port, retries_number=self.retries_number
        )
        self.topic = get_settings().kafka_settings.topic

    # def parse_request(request_for_ugs):

    def load(self, request_for_ugs: RequestForUGS):
        try:
            # ! TODO fix keys
            key = randint(10 ** 8, 10 ** 10)
            self.producer.send(
                topic=self.topic,
                key=str(key),
                value=request_for_ugs.dict(),
            )
            return True
        except KafkaError as kafka_error:
            logger.exception(kafka_error)
            return False


kafka_loader = KafkaLoader()
