from typing import Tuple, Union
from datetime import datetime

from humps import camelize
from pydantic import BaseModel as Model

from src.utils import convert_datetime_for_schemas


def to_camel(string):
    return camelize(string)


class BaseSchema(Model):
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: convert_datetime_for_schemas
        }
        default_exclude: Tuple = tuple()
        default_exclude_unset: Tuple = tuple()
        default_exclude_none: Tuple = tuple()
        arbitrary_types_allowed: bool = True

    def dict(self,
             *,
             include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None, # type: ignore
             exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None, # type: ignore
             by_alias: bool = False,
             skip_defaults: bool = None,
             exclude_unset: bool = False,
             exclude_defaults: bool = False,
             exclude_none: bool = False) -> 'DictStrAny': # type: ignore

        if hasattr(self.__config__, 'default_exclude') and self.__config__.default_exclude and not exclude:
            exclude = set(self.__config__.default_exclude)

        if hasattr(self.__config__, 'default_exclude_unset') and self.__config__.default_exclude_unset and not exclude_unset:
            exclude_unset = set(self.__config__.default_exclude_unset)

        if hasattr(self.__config__, 'default_exclude_none') and self.__config__.default_exclude_none and not exclude_none:
            exclude_none = set(self.__config__.default_exclude_none)

        return super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none
        )


class CamelSchema(BaseSchema):

    class Config:
        alias_generator = to_camel
