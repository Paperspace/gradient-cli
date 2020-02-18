from gradient.api_sdk import models
from gradient.api_sdk.serializers.base import BaseSchema

import marshmallow as ma

class ClusterSchema(BaseSchema):
    MODEL = models.Cluster
    id = ma.fields.String()
    name = ma.fields.String()
    type = ma.fields.String()
