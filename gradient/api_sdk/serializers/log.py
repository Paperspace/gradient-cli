import marshmallow

from .base import BaseSchema
from .. import models


class LogRowSchema(BaseSchema):
    MODEL = models.LogRow

    line = marshmallow.fields.Int()
    message = marshmallow.fields.Str()
    timestamp = marshmallow.fields.Str()
