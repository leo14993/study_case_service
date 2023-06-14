import redis

from typing import Union, Any

from src.infrastructure.cache_client.cache_client_abc import CacheClientABC
from src.settings.cache_settings import CacheSettings


class ClientCacheRedis(CacheClientABC):
    def __init__(self,
                 host: str = CacheSettings.CACHE_HOST,
                 port: int = CacheSettings.CACHE_PORT,
                 password=CacheSettings.CACHE_PASSWORD):
        is_ssl = password is not None
        self.client = redis.Redis(
            host=host,
            port=port,
            password=password,
            ssl=is_ssl
        )

    def get(self, key: str) -> Union[None, dict, str, bytes]:
        return self.client.get(name=key)

    def set(self, key: str, value: Any, ttl_seconds: int = None, ttl_milliseconds: int = None) -> None:
        if ttl_seconds:
            ttl_milliseconds = None
        self.client.set(
            name=key,
            value=value,
            ex=ttl_seconds,
            px=ttl_milliseconds
        )

    def set_if_not_exists(self, key: str, value: Any, ttl_seconds: int) -> bool:
        is_saved = self.client.setnx(
            name=key,
            value=value
        )
        if is_saved:
            self.client.expire(
                name=key,
                time=ttl_seconds
            )
        return is_saved

    def delete(self, key: str) -> bool:
        """
        Returns True if the key exists and had been deleted.
        Returns False if the key does not exist.
        """
        deleted = self.client.delete(key)
        exists_and_deleted = (deleted == 1)
        return exists_and_deleted
