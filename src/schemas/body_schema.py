from enum import Enum
from typing import Optional

from src.schemas.base import CamelSchema


class ReasonType(str, Enum):
    MY_REASON = 'my-reason'
    ANOTHER_REASON = 'another-reason'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, ReasonType))


class BodySchema(CamelSchema):
    reason: ReasonType
    my_version: Optional[str] = 'v2'