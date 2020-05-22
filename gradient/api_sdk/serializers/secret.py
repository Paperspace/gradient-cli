import marshmallow as ma

from .. import models
from ..serializers.base import BaseSchema


class SecretSchema(BaseSchema):
    MODEL = models.Secret

    name = ma.fields.Str()
