import logging

from models.event import EventForUGS


def transform(data):
    try:
        payload = EventForUGS(**data).dict()
        payload = payload | payload["payload"]
        event_type = payload["event_type"]
        for key in (
            "payload",
            "event_type",
        ):
            payload.pop(key)
    except Exception as transform_ex:
        logging.error("Error while transforming data: {0}".format(transform_ex))
    return event_type, payload or {}


def order_batches(data: list):
    organized_batches = {}
    for item in data:
        event_type, batch_item = item
        organized_batches[event_type].append(batch_item)
    return organized_batches
