import marshmallow

from .base import BaseSchema
from .. import models


class LogRowSchema(BaseSchema):
    MODEL = models.LogRow

    line = marshmallow.fields.Int()
    message = marshmallow.fields.Str()
    timestamp = marshmallow.fields.Str()

    @marshmallow.pre_load
    def rstrip_log_line(self, data):
        if "message" in data:
            data["message"] = str(data["message"]).rstrip()

        return data
