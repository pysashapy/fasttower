import tortoise
from tortoise.fields import *  # noqa: F403


class Model(tortoise.Model):
    id: int = tortoise.fields.IntField(pk=True)

    class Meta:
        abstract = True


__all__ = [
    'Model',

    "CASCADE",
    "RESTRICT",
    "SET_DEFAULT",
    "SET_NULL",
    "NO_ACTION",
    "OnDelete",
    "Field",
    "BigIntField",
    "BinaryField",
    "BooleanField",
    "CharEnumField",
    "CharField",
    "DateField",
    "DatetimeField",
    "TimeField",
    "DecimalField",
    "FloatField",
    "IntEnumField",
    "IntField",
    "JSONField",
    "SmallIntField",
    "SmallIntField",
    "TextField",
    "TimeDeltaField",
    "UUIDField",
    "BackwardFKRelation",
    "BackwardOneToOneRelation",
    "ForeignKeyField",
    "ForeignKeyNullableRelation",
    "ForeignKeyRelation",
    "ManyToManyField",
    "ManyToManyRelation",
    "OneToOneField",
    "OneToOneNullableRelation",
    "OneToOneRelation",
    "ReverseRelation",
]
