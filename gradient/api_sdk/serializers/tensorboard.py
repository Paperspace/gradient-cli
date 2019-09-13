import marshmallow
from enum import Enum
from marshmallow.validate import OneOf

from . import BaseSchema
from .. import models


class InstanceType(Enum):
    CPU = 'cpu'
    GPU = 'gpu'


class InstanceSize(Enum):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = 'large'


class InstanceSchema(BaseSchema):
    MODEL = models.Instance

    type = marshmallow.fields.String(validate=marshmallow.validate.OneOf(choices=[e.value for e in InstanceType]))
    size = marshmallow.fields.String(validate=marshmallow.validate.OneOf(choices=[e.value for e in InstanceSize]))
    count = marshmallow.fields.Int()


class TensorboardSchema(BaseSchema):
    MODEL = models.Tensorboard

    id = marshmallow.fields.Str()
    image = marshmallow.fields.Str()
    username = marshmallow.fields.Str()
    password = marshmallow.fields.Str()
    instance = marshmallow.fields.Nested(InstanceSchema, required=False, default=None)
    experiments = marshmallow.fields.List(marshmallow.fields.String())
    url = marshmallow.fields.Str()
    state = marshmallow.fields.Int()
