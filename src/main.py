import inject
import traceback
from http import HTTPStatus

from fastapi import Request
from starlette.responses import JSONResponse


from src.app import make_app
from src.context_request import context_request
from src.infrastructure.database.sql_alchemy import DatabaseAdapter
from src.settings import adapter_binders
from src.settings.app_settings import AppSettings

app = make_app(
    on_startup_funcs=[

    ],
    on_shutdown_func=[

    ]
)


@app.middleware("http")
async def middleware_http(request: Request, call_next) -> JSONResponse:
    request_id = context_request.set(request)
    database = DatabaseAdapter()
    try:
        response = await call_next(request)

        context_request.reset(request_id)

        return response

    except Exception as e:
        if AppSettings.is_development_environment() or AppSettings.is_local_environment():
            traceback.print_exc()

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content={'detail': 'Ocorreu um erro inesperado.'}
        )
    finally:
        await database.terminate()


def configure(binder):
    for config in adapter_binders:
        config(binder, app)


inject.configure_once(configure, bind_in_runtime=False)
