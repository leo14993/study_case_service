from http import HTTPStatus
from fastapi import Response, APIRouter

router = APIRouter()
prefix = ''
tags = ['Misc']


@router.get("/health-check", status_code=HTTPStatus.OK)
async def health_check(response: Response):
    
    return {'resources': 'Health check'}
