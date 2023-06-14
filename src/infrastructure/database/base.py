from abc import ABC
from typing import Union

from fastapi import FastAPI


class Adapter(ABC):

    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.post_init()

    def post_init(self) -> None:
        pass  # This function is to put something that needs to be executed as soon as the class is instantiated


class ApplicationStateMixin(Adapter):

    STATE_NAME: Union[str, None] = None

    def post_init(self) -> None:
        if self.STATE_NAME is None:
            raise ValueError('STATE NAME not defined')

        if not self.STATE_NAME:
            raise ValueError('STATE NAME is empty')

        app: FastAPI = getattr(self, 'app', None)

        if app:
            setattr(app.state, self.STATE_NAME, self)

    @classmethod
    def get_instance(cls, app: FastAPI) -> object:
        try:
            return getattr(app.state, cls.STATE_NAME)
        except AttributeError:
            return cls(None)

    async def init(self):
        raise NotImplementedError

    async def terminate(self):
        raise NotImplementedError
