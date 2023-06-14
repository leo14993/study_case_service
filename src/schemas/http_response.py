from typing import Dict, Optional

from src.schemas.base import CamelSchema


class HttpResponse(CamelSchema):
    status_code: int
    json_response: Optional[Dict]
