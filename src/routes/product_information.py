from http import HTTPStatus
from typing import Union, Optional

import inject
from fastapi import Response, APIRouter, Header, Request, Query
from pydantic.types import UUID4

from src.schemas.body_schema import BodySchema
from src.schemas.utils import NotFoundResponse
from src.services.product_service import ProductService

router = APIRouter()
prefix = '/information'
tags = ['Product Information']


@router.post(
    "/{information_id}/products/{product_id}",
    status_code=HTTPStatus.OK,
    response_description='Retorna a informação do produto',
    responses={
        HTTPStatus.NOT_FOUND.value: {
            'model': NotFoundResponse,
            'description': 'Registro de Simulação não encontrado'
        },
    },
    name='Retorna a informação do produto'
)
async def offer_detail(information_id: UUID4, product_id: Optional[str],
                       body: BodySchema,
                       request: Request,
                       response: Response,
                       partners: Optional[str] = Query(default=None),
                       has_debts_flag: Optional[bool] = Query(default=None, alias='hasDebtsFlag'),
                       x_user_id: Union[str, None] = Header(default=None, alias='x-user-id'),

                       ):
    product_service: ProductService = inject.instance(ProductService)

    return await product_service.retrieve_product(str(information_id), str(product_id), body)
