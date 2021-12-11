from functools import lru_cache

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8000, env="PORT")
    is_debug: bool = Field(True, env="DEBUG")
    should_reload: bool = Field(True, env="SHOULD_RELOAD")


class KafkaSettings(BaseSettings):
    hosts: list[str] = Field(["127.0.0.1:29092"], env="KAFKA_HOSTS")
    topic: str = Field("movie_topic", env="KAFKA_TOPIC")


class Settings(BaseSettings):
    app = AppSettings()
    kafka_settings = KafkaSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
