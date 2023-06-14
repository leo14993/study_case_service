from typing import Optional, Dict

import inject


from src.enums import CacheExpire
from src.exceptions import NotFoundException
from src.infrastructure.cache_client.io_redis import ClientCacheIORedis
from src.infrastructure.database.sql_alchemy import DatabaseAdapter
from src.schemas.body_schema import BodySchema
from src.schemas.information_schema import InformationSchema
from src.models.product import Product
from src.models.information import Information
from src.services.feature_flag_service import FeatureFlagService


def cache_first(function):

    async def apply_cache(*args):

        key = f'cache-prefix:{args[1]}:{args[2]}'

        data = await args[0].cache.get(key)
        if data:
            return data
        data = await function(*args)

        if data:
            await args[0].cache.save(key, data, CacheExpire.HOUR)

        return data

    return apply_cache


class ProductService:
    product: Product = Product
    information: Information = Information
    db: DatabaseAdapter = inject.attr(DatabaseAdapter)
    cache: ClientCacheIORedis = inject.attr(ClientCacheIORedis)
    feature_flag_service: FeatureFlagService = inject.attr(FeatureFlagService)

    @cache_first
    async def retrieve_product(self, information_id: str, product_id: str, information_input_data: BodySchema) -> Dict:
        product = await self.db.get_by_id(self.product, product_id)
        information = await self.db.get_by_id(self.information, information_id)

        feature_flags = await self.feature_flag_service.get_feature_flag_treatments(
            information_input_data.dict(by_alias=True)
        )

        if not information:
            raise NotFoundException

        information = InformationSchema.from_orm(information)

        products_from_information = self.get_products_from_information(information, product_id)

        return {
            "data": {
                "information": information,
                "product": product,
                "products_from_information": products_from_information,
                "flags": feature_flags
            }
        }

    @classmethod
    def get_products_from_information(cls, information: Optional[InformationSchema], product_id: str) -> Dict:
        products = []
        product_information = {}

        if information:
            products = information.products

        for product in products:
            if product['id'] == product_id:
                product_information = product
                break

        return product_information

