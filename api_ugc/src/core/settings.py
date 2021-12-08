from datetime import timedelta
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    host: str = Field("127.0.0.1", env="HOST")
    port: int = Field(8000, env="PORT")
    is_debug: bool = Field(True, env="DEBUG")

    jwt_algorithms = Field("HS256", env="JWT_SECRET_KEY")  # jwt
    jwt_public_key = Field("jwt_public_key", env="JWT_SECRET_KEY")


class KafkaSettings(BaseSettings):
    host: str = Field("127.0.0.1", env="KAFKA_HOST")
    port: int = Field(6379, env="KAFKA_PORT")


class Settings(BaseSettings):
    app = AppSettings()
    kafka_settings = KafkaSettings()


@lru_cache
def get_settings():
    return Settings()
