from typing import Dict, Optional

from pydantic import BaseModel


class SqsMessageModel(BaseModel):
    endpoint: str
    headers: Dict
    payload: Dict
    settings: Optional[Dict] = {}
    partner: Optional[str]


class SqsReceivedMessageModel(BaseModel):
    data:  Dict
    receipt_handle: str
