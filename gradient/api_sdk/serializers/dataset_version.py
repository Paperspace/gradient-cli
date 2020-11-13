import marshmallow as ma

from .. import models
from ..serializers.base import BaseSchema


class DatasetVersionSummarySchema(BaseSchema):
    MODEL = models.DatasetVersionTagSummary

    name = ma.fields.Str()


class DatasetVersionSchema(BaseSchema):
    MODEL = models.DatasetVersion

    version = ma.fields.Str()
    message = ma.fields.Str()
    is_committed = ma.fields.Bool(load_from="isCommitted", dump_to="isCommitted")
    tags = ma.fields.Nested(DatasetVersionSummarySchema, load_only=True, many=True)

    dataset_id = ma.fields.Str(dump_to="id", dump_only=True)


class DatasetVersionPreSignedURLSchema(BaseSchema):
    MODEL = models.DatasetVersionPreSignedURL

    url = ma.fields.Str()
    expires_in = ma.fields.Integer()
