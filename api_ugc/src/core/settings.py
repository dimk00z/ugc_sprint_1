from functools import lru_cache

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8000, env="PORT")
    is_debug: bool = Field(True, env="DEBUG")
    should_reload: bool = Field(True, env="SHOULD_RELOAD")

    jwt_algorithms = Field("HS256", env="JWT_SECRET_KEY")  # jwt
    jwt_public_key = Field("jwt_public_key", env="JWT_SECRET_KEY")


class KafkaSettings(BaseSettings):
    host: str = Field("127.0.0.1", env="KAFKA_HOST")
    port: int = Field(29092, env="KAFKA_PORT")
    topic: str = Field("movie_topic", env="KAFKA_TOPIC")
    retries_number: int = Field(5, env="KAFKA_RETRIES_NUMBER")


class Settings(BaseSettings):
    app = AppSettings()
    kafka_settings = KafkaSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
