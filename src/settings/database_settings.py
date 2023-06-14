from typing import Dict

from decouple import config


class _DatabaseSettings:
    DATABASE_URL: str
    POOL_RECYCLE: int
    POOL_SIZE: int
    AUTOCOMMIT: bool
    AUTOFLUSH: bool
    DEBUG: bool

    @classmethod
    def get_engine_kwargs(cls) -> Dict:
        return {
            'pool_recycle': cls.POOL_RECYCLE,
            'pool_size': cls.POOL_SIZE,
            'echo': cls.DEBUG,
        }

    @classmethod
    def get_database_url(cls) -> str:
        if cls.DATABASE_URL.startswith('pgsql://'):
            cls.DATABASE_URL = cls.DATABASE_URL.replace('pgsql://', 'postgresql://')

        return cls.DATABASE_URL

    @classmethod
    def get_session_kwargs(cls) -> Dict:
        return {
            'autocommit': cls.AUTOCOMMIT,
            'autoflush': cls.AUTOFLUSH,
        }


class DatabaseSettings(_DatabaseSettings):
    DATABASE_URL = config('DATABASE_URL', default='postgresql://postgres:password@localhost:5432/my_table')
    POOL_RECYCLE = config('DATABASE_POOL_RECYCLE_PERIOD', default=-1, cast=int)
    POOL_SIZE = config('DATABASE_POOL_SIZE', default=10, cast=int)
    AUTOCOMMIT = config('DATABASE_AUTOCOMMIT', default=False, cast=bool)
    AUTOFLUSH = config('DATABASE_AUTOFLUSH', default=False, cast=bool)
    DEBUG = config('DATABASE_DEBUG', default=False, cast=bool)
