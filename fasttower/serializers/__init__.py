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

        # Обработка вложенных сериализаторов
        for field in self.Config.fields:
            field_type = self.__annotations__.get(field)
            if isinstance(field_type, type) and issubclass(field_type, ModelSerializer):
                related_instances = getattr(instance, field)
                if isinstance(related_instances, list):
                    data[field] = [field_type(pet) for pet in related_instances]
                elif related_instances:
                    data[field] = field_type(related_instances)
                else:
                    data[field] = None

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
        for field_name in fields:
            field = model._meta.fields_map.get(field_name, None)
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
