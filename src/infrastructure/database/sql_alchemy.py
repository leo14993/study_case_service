from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta as Base
from sqlalchemy.exc import NoResultFound

from starlette.requests import Request

from typing import Union, Optional, Callable

from src.context_request import context_request
from src.infrastructure.database.base import ApplicationStateMixin, Adapter
from src.settings.database_settings import DatabaseSettings

engine = create_engine(DatabaseSettings.get_database_url(), **DatabaseSettings.get_engine_kwargs())
Session = sessionmaker(bind=engine, **DatabaseSettings.get_session_kwargs())
SqlBase = declarative_base()


class DatabaseAdapter(ApplicationStateMixin):
    session: Session = None
    STATE_NAME = 'DB'

    def __init__(self, **kwargs) -> None:
        Adapter.__init__(self, **kwargs)
        self.session = Session()

    async def terminate(self) -> None:
        if self.session is not None:
            try:
                self.session.close()
            except Exception:
                self.session.rollback()
                self.session.close()
            self.session = None

    async def get_by_id(self, model: Base, value: Union[str, int], id_name: str = 'id') -> Optional[Base]:
        field = getattr(model, id_name)
        try:

            obj = self.session.query(model).filter(field == value).one()
            return obj

        except NoResultFound:
            return None

    def post_init(self) -> None:
        if self.STATE_NAME is None:
            raise ValueError('STATE NAME not defined')

        if not self.STATE_NAME:
            raise ValueError('STATE NAME is empty')

        request: Request = context_request.get('context_request')

        if request:
            setattr(request.state, self.STATE_NAME, self)

    @classmethod
    def get_instance(cls, **kwargs) -> object:
        try:
            request: Request = context_request.get('context_request')
            return getattr(request.state, cls.STATE_NAME)
        except AttributeError:
            return cls()


def startup_database(app: FastAPI) -> Callable:
    async def _inner():
        database = DatabaseAdapter(app=app)
        await database.init()

    return _inner


def shutdown_database(app: FastAPI) -> Callable:
    async def _inner():
        database = DatabaseAdapter.get_instance(app)
        await database.terminate()

    return _inner
