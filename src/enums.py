import enum
from math import ceil
from datetime import datetime, timedelta

from src.utils import get_default_tzinfo, get_america_datetime


class AuthHeaders(str, enum.Enum):
    USER = 'X-USER-ID'


class CacheExpire:
    MIN = 60
    TWENTY_MIN = 1200
    THIRTY_MIN = 1800
    HOUR = 3600
    TWELVE_HOURS = 43200
    DAY = 86400
    WEEK = 604800

    @classmethod
    def days(cls, quantity: int) -> int:
        return cls.DAY * quantity

    @staticmethod
    def midnight() -> int:
        now = get_america_datetime()
        temp_date = now + timedelta(days=1)
        midnight = datetime(
            temp_date.year,
            temp_date.month,
            temp_date.day,
            0,
            0,
            0,
            tzinfo=get_default_tzinfo()
        )
        interval = midnight - now

        return ceil(interval.total_seconds())

