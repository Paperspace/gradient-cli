import marshmallow as ma

from .base import BaseSchema
from .tag import TagSchema
from .. import models


class VolumeOptionsSchema(BaseSchema):
    MODEL = models.VolumeOptions

    kind = ma.fields.Str(required=True)
    size = ma.fields.Str(required=True)


class ExperimentDatasetSchema(BaseSchema):
    MODEL = models.ExperimentDataset

    id = ma.fields.String()
    uri = ma.fields.String()
    aws_access_key_id = ma.fields.String(dump_to="awsAccessKeyId", load_from="awsAccessKeyId")
    aws_secret_access_key = ma.fields.String(dump_to="awsSecretAccessKey", load_from="awsSecretAccessKey")
    aws_endpoint = ma.fields.String(dump_to="awsEndpoint", load_from="awsEndpoint")
    etag = ma.fields.String()
    version_id = ma.fields.String(dump_to="versionId", load_from="versionId")
    name = ma.fields.String()
    tags = ma.fields.Nested(TagSchema, only="name", many=True, load_only=True)
    volume_options = ma.fields.Nested(VolumeOptionsSchema, dump_to="volumeOptions", load_from="volumeOptions")
