
from decouple import config


class CacheSettings:
    CACHE_HOST = config('CACHE_HOST', default='localhost')
    CACHE_PORT = config('CACHE_PORT', default=6379)
    CACHE_PASSWORD = config('CACHE_PASSWORD', default=None)
    POOL_MAX_SIZE = config('CACHE_POOL_MAX_SIZE', default=10, cast=int)
    PREFIX = config('CACHE_PREFIX', default='cache-prefix')

    @classmethod
    def get_url(cls):
        scheme = 'rediss' if cls.CACHE_PASSWORD else 'redis'
        return f'{scheme}://:{cls.CACHE_PASSWORD}@{cls.CACHE_PORT}:{cls.CACHE_HOST}'

