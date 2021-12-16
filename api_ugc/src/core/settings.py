from functools import lru_cache

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8000, env="PORT")
    is_debug: bool = Field(True, env="DEBUG")
    should_reload: bool = Field(True, env="SHOULD_RELOAD")

    should_check_auth: bool = Field(False, env="SHOULD_CHECK_AUTH")
    auth_host = Field("http://localhost:8001/", env="AUTH_HOST")
    jwt_public_key = Field("JWT_PUBLIC_KEY", env="JWT_PUBLIC_KEY")
    jwt_algorithm = Field("HS256", env="JWT_ALGORITHM")


class KafkaSettings(BaseSettings):
    hosts: list[str] = Field(["127.0.0.1:29092"], env="KAFKA_HOSTS")
    topic: str = Field("movie_topic", env="KAFKA_TOPIC")
    project_name: str = Field("movie_kafka_producer", env="PROJECT_NAME")


class RedisSettings(BaseSettings):
    ttl: int = Field(60 * 5, env="REDIS_TTL")
    endpoint: str = Field("127.0.0.1", env="REDIS_HOST")
    port: int = Field(6379, env="REDIS_PORT")
    pool_min_size: int = 5
    pool_max_size: int = 10
    noself: bool = True


class Settings(BaseSettings):
    app = AppSettings()
    kafka_settings = KafkaSettings()
    redis_settings = RedisSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
