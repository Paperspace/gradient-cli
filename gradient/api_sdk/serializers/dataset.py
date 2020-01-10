import marshmallow as ma

from .base import BaseSchema


class DatasetSchema(BaseSchema):
    uri = ma.fields.String(required=True)
    aws_access_key_id = ma.fields.String(dump_to="awsAccessKeyId", load_from="awsAccessKeyId")
    aws_secret_access_key = ma.fields.String(dump_to="awsSecretAccessKey", load_from="awsSecretAccessKey")
    etag = ma.fields.String()
    version_id = ma.fields.String(dump_to="versionId", load_from="versionId")
    name = ma.fields.String()
