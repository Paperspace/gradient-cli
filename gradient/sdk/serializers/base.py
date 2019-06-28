import marshmallow


class BaseSchema(marshmallow.Schema):
    @marshmallow.post_dump
    def remove_none_values(self, data):
        return {
            key: value for key, value in data.items()
            if value is not None
        }
