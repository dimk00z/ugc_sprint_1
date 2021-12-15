from datetime import datetime
from random import choice, randint
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel


class Payload(BaseModel):
    movie_id: UUID
    user_id: UUID
    event: str
    event_data: Optional[str]
    event_timestamp: int

    def dict(self, *args, **kwargs):
        result: dict = super().dict(*args, **kwargs)
        result["movie_id"] = str(result["movie_id"])
        result["user_id"] = str(result["user_id"])
        return result


class EventForUGS(BaseModel):
    payload: Payload
    language: Optional[str]
    timezone: Optional[str]
    ip: Optional[str]
    version: Optional[str]
    client_data: Optional[str]


def create_random_event() -> EventForUGS:
    request: EventForUGS = EventForUGS(
        language=choice(("ru", "en", "fr")),
        timezone=f"gmt+{randint(0,12)}",
        ip=f"{randint(0,254)}.{randint(0,254)}.{randint(0,254)}.{randint(0,254)}",
        version="1.0",
        payload=Payload(
            movie_id=uuid4(),
            user_id=uuid4(),
            event=choice(("skipped", "commented", "finished")),
            event_data="event_data",
            event_timestamp=int(datetime.now().timestamp()),
        ),
    )
    return request
