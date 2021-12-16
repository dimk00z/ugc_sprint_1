import json
import logging
from random import choice
from uuid import uuid4

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError
from models.event import EventForUGS

from core.settings import get_settings

logger = logging.getLogger(__name__)


class UGCKafkaProducer:
    @staticmethod
    def serializer(value):
        return json.dumps(value).encode()

    def __init__(self) -> None:
        self.hosts = ",".join(get_settings().kafka_settings.hosts)
        self.topic = get_settings().kafka_settings.topic

    def _get_key(self) -> str:
        return str(uuid4()).encode()

    async def produce(self, request_for_ugs: EventForUGS, producer: AIOKafkaProducer):
        was_produced = False
        try:
            key = self._get_key()
            await producer.send(self.topic, request_for_ugs.dict(), key=key)
            was_produced = True
            logger.info("Message sent with uuid=%s", key.decode())
        except KafkaError as kafka_error:
            logger.exception(kafka_error)
        return was_produced

    async def send_batch(self, producer, batch):
        partitions = await producer.partitions_for(self.topic)
        partition = choice(tuple(partitions))
        await producer.send_batch(batch, self.topic, partition=partition)
        logger.info(
            "%d messages sent to partition %d" % (batch.record_count(), partition)
        )

    async def batch_produce(
        self, requests: list[EventForUGS], producer: AIOKafkaProducer
    ):
        was_produced = False
        try:
            batch = producer.create_batch()
            submission = 0
            while submission < len(requests):
                metadata = batch.append(
                    key=self._get_key(),
                    value=UGCKafkaProducer.serializer(requests[submission].dict()),
                    timestamp=None,
                )
                if metadata is None:
                    await self.send_batch(producer=producer, batch=batch)
                    batch = producer.create_batch()
                    continue
                submission += 1
            await self.send_batch(producer=producer, batch=batch)
            was_produced = True
        except KafkaError as kafka_error:
            logger.exception(kafka_error)
        return was_produced


ugc_kafka_producer = UGCKafkaProducer()
