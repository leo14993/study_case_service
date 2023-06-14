from __future__ import annotations

from typing import List, Union, Optional

from src.schemas.base import CamelSchema


class KeyValue(CamelSchema):
    key: str
    value: Optional[Union[str, int, float, List]]


class LabelValue(CamelSchema):
    label: str
    value: Optional[Union[str, int, float, List]]


class NotFoundResponse(CamelSchema):
    detail: str = 'Item não encontrado'
