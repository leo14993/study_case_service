from pydantic import BaseModel


class BaseResultModel(BaseModel):
    def dict(self, *args, **kwargs):
        result = super().dict(*args, **kwargs)
        result_dict = {'result': result}
        return result_dict


class BaseSerializerModel(BaseModel):
    class Config:
        allow_population_by_field_name = True
