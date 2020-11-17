import marshmallow as ma

from .. import models
from ..serializers.base import BaseSchema
from .dataset_version import DatasetVersionSchema
from .storage_provider import StorageProviderSchema


class DatasetSchema(BaseSchema):
    MODEL = models.Dataset

    id = ma.fields.Str()
    name = ma.fields.Str()
    description = ma.fields.Str()
    storage_provider_id = ma.fields.Str(dump_to="storageProviderId", dump_only=True)
    storage_provider = ma.fields.Nested(StorageProviderSchema, load_from="storageProvider", load_only=True)


class DatasetRefSchema(DatasetSchema):
    MODEL = models.DatasetRef

    version = ma.fields.Nested(DatasetVersionSchema, load_only=True)
