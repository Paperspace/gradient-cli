from gradient.api_sdk.serializers.base import BaseSchema

import marshmallow as ma

class ClusterSchema(BaseSchema):
    id = ma.fields.String()
    name = ma.fields.String()
    type = ma.fields.String()
