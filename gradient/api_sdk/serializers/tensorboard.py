from enum import Enum

import marshmallow
from marshmallow.validate import OneOf

from .base import BaseSchema
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


class TBExperimentSchema(BaseSchema):
    id = marshmallow.fields.String()
    project_id = marshmallow.fields.String()
    state = marshmallow.fields.String()


class TensorboardDetailSchema(BaseSchema):
    MODEL = models.Tensorboard

    id = marshmallow.fields.Str()
    image = marshmallow.fields.Str()
    username = marshmallow.fields.Str()
    password = marshmallow.fields.Str()
    instance = marshmallow.fields.Nested(InstanceSchema, required=False, default=None)
    experiments = marshmallow.fields.List(marshmallow.fields.Nested(TBExperimentSchema))
    url = marshmallow.fields.Str()
    state = marshmallow.fields.String()


class TensorboardSchema(BaseSchema):
    MODEL = models.Tensorboard

    id = marshmallow.fields.Str()
    image = marshmallow.fields.Str()
    username = marshmallow.fields.Str()
    password = marshmallow.fields.Str()
    instance = marshmallow.fields.Nested(InstanceSchema, required=False, default=None)
    experiments = marshmallow.fields.List(marshmallow.fields.String())
    url = marshmallow.fields.Str()
    state = marshmallow.fields.String()
