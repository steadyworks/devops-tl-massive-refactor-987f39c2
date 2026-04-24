import os

from redis.asyncio import ConnectionPool, Redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry

from backend.lib.utils.common import none_throws


class RedisClient:
    def __init__(self) -> None:
        self.__connection_pool = ConnectionPool(
            host=none_throws(os.getenv("REDIS_HOST")),
            port=int(none_throws(os.getenv("REDIS_PORT"))),
            username=none_throws(os.getenv("REDIS_USERNAME")),
            password=none_throws(os.getenv("REDIS_PASSWORD")),
            decode_responses=True,
            socket_keepalive=True,
            health_check_interval=30,  # pings periodically to detect dead conns
            retry=Retry(ExponentialBackoff(), retries=5),  # retries on disconnect
        )
        self.client = Redis(
            connection_pool=self.__connection_pool,
            decode_responses=True,
        )
