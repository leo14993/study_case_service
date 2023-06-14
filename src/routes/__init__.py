from fastapi import  APIRouter

from src.routes import product_information, misc
from src.settings.app_settings import AppSettings

app_router = APIRouter()


# Misc routes
app_router.include_router(
    misc.router,
    prefix=f'{AppSettings.BASE_PATH}{misc.prefix}',
    tags=misc.tags
)

app_router.include_router(
    product_information.router,
    prefix=f'{AppSettings.BASE_PATH}/v1/{product_information.prefix}',
    tags=product_information.tags
)


