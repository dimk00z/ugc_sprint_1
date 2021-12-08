from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Payload(BaseModel):
    movie_id: UUID
    user_id: UUID
    event: str
    event_data: Optional[str]
    event_timestamp: int


class RequestForUGS(BaseModel):
    payload: Payload
    language: Optional[str]
    timezone: Optional[str]
    ip: Optional[str]
    version: Optional[str]
    client_data: Optional[str]
