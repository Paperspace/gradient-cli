import marshmallow as ma

from gradient.api_sdk.serializers.base import BaseSchema
from .. import models


class TagSchema(BaseSchema):
    MODEL = models.Tag

    name = ma.fields.Str()
