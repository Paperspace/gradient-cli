import marshmallow as ma

from .. import models
from ..serializers.base import BaseSchema


class StorageProviderSchema(BaseSchema):
    MODEL = models.StorageProvider

    id = ma.fields.Str()
    type = ma.fields.Str()
    name = ma.fields.Str()
    config = ma.fields.Dict()
