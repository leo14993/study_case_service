from typing import Optional
from pydantic import BaseModel


class Request(BaseModel):
    method: str
    url: str
    status_code: int
    process_time: float
    alias: Optional[str]
