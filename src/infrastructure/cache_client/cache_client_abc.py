from abc import ABC
from typing import Any


class CacheClientABC(ABC):
    def get(self, key: str) -> None:
        raise NotImplementedError('Cache client get not implemented')

    def set(self, key: str, value: Any, ttl_seconds: int = None, ttl_milliseconds: int = None) -> None:
        raise NotImplementedError('Cache client set not implemented')

    def set_if_not_exists(self, key: str, value: Any, ttl_seconds: int) -> bool:
        raise NotImplementedError('Cache client setnx not implemented')

    def delete(self, key: str) -> bool:
        raise NotImplementedError('Cache client delete not implemented')
