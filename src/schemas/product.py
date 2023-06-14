from __future__ import annotations

from typing import Optional, List

from pydantic import Field

from src.schemas.base import CamelSchema


class ProductSimulationSchema(CamelSchema):
    id: int
    status: int
    description: Optional[str]
    partner_business_name: Optional[str] = Field(..., alias='partner-business-name')
    partner_name: Optional[str]


