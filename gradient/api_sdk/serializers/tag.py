import marshmallow as ma

from .. import models
from ..serializers.base import BaseSchema


class TagSchema(BaseSchema):
    MODEL = models.Tag

    name = ma.fields.Str()
