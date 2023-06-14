from typing import Optional, Dict, List, Any

from pydantic import Field

from src.schemas.base import CamelSchema


class InformationSchema(CamelSchema):
    id: str = Field(..., title='Id')
    offers: Optional[List[Dict]] = Field(None, title='Offers')
    suggestion: Optional[bool] = Field(None, title='Suggestion')
    adjusted: Optional[bool] = Field(None, title='Adjusted')
    products: Optional[List[Dict]] = Field(None, title='Products')

    class Config:
        orm_mode = True