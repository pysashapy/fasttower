from datetime import datetime, date, time
from pydantic import BaseModel, ConfigDict
from typing import Unpack, Any

from fasttower.db import models

tortoise_to_pydantic_types = {
    models.IntField: int,
    models.CharField: str,
    models.BooleanField: bool,
    models.DatetimeField: datetime,
    models.FloatField: float,
    models.DecimalField: float,
    models.DateField: date,
    models.TimeField: time,
}


class Serializer(BaseModel):
    pass


class ModelSerializer(BaseModel):
    class Config:
        model = None
        fields = []

    def __init__(self, instance: Any, **kwargs):
        self.instance = instance
        data = {field: getattr(instance, field) for field in self.Config.fields}
        super().__init__(**kwargs, **data)

    def __str__(self):
        field_values = ', '.join(
            f"{field}={getattr(self, field)!r}" for field in self.Config.fields
        )
        return f"{self.__class__.__name__}({field_values})"

    @classmethod
    def __init_subclass__(cls, **kwargs: Unpack[ConfigDict]):
        super().__init_subclass__(**kwargs)
        config = getattr(cls, 'Config', None)
        model = config.model
        fields = config.fields
        print('АЛЕЕЕ!"1111111111111№', fields)
        for field_name in fields:
            field = model._meta.fields_map.get(field_name, None)
            print(field)
            if isinstance(field, models.Field):
                pydantic_type = cls.get_pydantic_field_type(field)
                if pydantic_type:
                    cls.__annotations__[field_name] = pydantic_type
            else:
                raise ValueError(f"Field '{field_name}' not found in model '{model.__name__}'")

    @staticmethod
    def get_pydantic_field_type(field):
        for tortoise_type, pydantic_type in tortoise_to_pydantic_types.items():
            if isinstance(field, tortoise_type):
                return pydantic_type
        return None
