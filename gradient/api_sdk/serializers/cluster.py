import marshmallow as ma

from gradient.api_sdk.serializers.base import BaseSchema


class ClusterSchema(BaseSchema):
    id = ma.fields.String()
    name = ma.fields.String()
    type = ma.fields.String()
