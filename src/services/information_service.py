from typing import Optional, Dict

import inject

from src.infrastructure.http_client.httpx.http_client import HttpClient
from src.schemas.product import ProductSimulationSchema
from src.settings.app_settings import ProductSettings


class InformationService:

    @staticmethod
    async def get_product_details(product: Optional[ProductSimulationSchema]) -> Optional[Dict]:
        http_adapter: HttpClient = inject.instance(HttpClient)

        response = await http_adapter.get(
            f'{ProductSettings.HOST}/v1/products/{product.id}',
            headers={
            }
        )
        return response.payload
