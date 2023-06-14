from typing import List, Callable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import app_router

from src.exceptions import UnicornException, unicorn_exception_handler
from src.settings.app_settings import AppSettings


def make_app(on_startup_funcs: List[Callable] = [], on_shutdown_func: List[Callable] = []) -> FastAPI:
    app = FastAPI(
        title=AppSettings.TITLE,
        version=AppSettings.VERSION,
        description=AppSettings.DESCRIPTION,
        debug=AppSettings.DEBUG,
        openapi_url=f"{AppSettings.BASE_PATH}/openapi.json",
        docs_url=f"{AppSettings.BASE_PATH}/docs",
        redoc_url=f"{AppSettings.BASE_PATH}/redoc",
        exception_handlers={
            UnicornException: unicorn_exception_handler
        }
    ) 

    app.include_router(app_router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for func in on_startup_funcs:
        app.router.on_startup.append(func(app))
    
    for func in on_shutdown_func:
        app.router.on_shutdown.append(func(app))

    return app
