import marshmallow

from gradient.api_sdk import models
from .base import BaseSchema


class LogRowSchema(BaseSchema):
    MODEL = models.LogRow

    line = marshmallow.fields.Int()
    message = marshmallow.fields.Str()
    timestamp = marshmallow.fields.Str()
