import aioredis
from typing import Union, Any
from src.infrastructure.cache_client.cache_client_abc import CacheClientABC
from src.settings.cache_settings import CacheSettings


class ClientCacheIORedis(CacheClientABC):
    def __init__(self,
                 host: str = CacheSettings.CACHE_HOST,
                 port: int = CacheSettings.CACHE_PORT,
                 password: str = CacheSettings.CACHE_PASSWORD):
        is_ssl = password is not None
        self.client = aioredis.Redis(
            host=host,
            port=port,
            password=password,
            ssl=is_ssl,
            max_connections=CacheSettings.POOL_MAX_SIZE
        )

    async def get(self, key: str) -> Union[None, dict, str, bytes]:
        return await self.client.get(name=key)

    async def set(self, key: str, value: Any, ttl_seconds: int = None, ttl_milliseconds: int = None) -> None:
        if ttl_seconds:
            ttl_milliseconds = None
        await self.client.set(
            name=key,
            value=value,
            ex=ttl_seconds,
            px=ttl_milliseconds
        )

    async def set_if_not_exists(self, key: str, value: Any, ttl_seconds: int) -> bool:
        is_saved = await self.client.setnx(
            name=key,
            value=value
        )
        if is_saved:
            await self.client.expire(
                name=key,
                time=ttl_seconds
            )
        return is_saved

    async def delete(self, key: str) -> bool:
        """
        Returns True if the key exists and had been deleted.
        Returns False if the key does not exist.
        """
        deleted = await self.client.delete(key)
        exists_and_deleted = (deleted == 1)
        return exists_and_deleted
