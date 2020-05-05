import marshmallow as ma

from .. import models
from ..serializers.base import BaseSchema


class ClusterSchema(BaseSchema):
    MODEL = models.Cluster
    id = ma.fields.String()
    name = ma.fields.String()
    type = ma.fields.String()
