import marshmallow as ma

from .base import BaseSchema
from .tag import TagSchema
from .. import models


class DatasetVolumeOptionsSchema(BaseSchema):
    kind = ma.fields.Str(required=True)
    size = ma.fields.Str(required=True)


class DatasetSchema(BaseSchema):
    MODEL = models.Dataset

    uri = ma.fields.String(required=True)
    aws_access_key_id = ma.fields.String(dump_to="awsAccessKeyId", load_from="awsAccessKeyId")
    aws_secret_access_key = ma.fields.String(dump_to="awsSecretAccessKey", load_from="awsSecretAccessKey")
    etag = ma.fields.String()
    version_id = ma.fields.String(dump_to="versionId", load_from="versionId")
    name = ma.fields.String()
    tags = ma.fields.Nested(TagSchema, only="name", many=True, load_only=True)
    volume_options = ma.fields.Nested(DatasetVolumeOptionsSchema, dump_to="volumeOptions", load_from="volumeOptions")
