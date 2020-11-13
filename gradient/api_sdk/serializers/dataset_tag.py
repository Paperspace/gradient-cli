import marshmallow as ma

from .. import models
from ..serializers.base import BaseSchema


class DatasetVersionSummarySchema(BaseSchema):
    MODEL = models.DatasetVersionSummary

    version = ma.fields.Str()
    message = ma.fields.Str()


class DatasetTagSchema(BaseSchema):
    MODEL = models.DatasetTag

    name = ma.fields.Str()
    version = ma.fields.Nested(DatasetVersionSummarySchema, load_only=True)
