import marshmallow


class BaseSchema(marshmallow.Schema):
    MODEL = None

    @marshmallow.post_dump
    def remove_none_values(self, data):
        return {
            key: value for key, value in data.items()
            if value is not None
        }

    def get_instance(self, obj_dict):
        if not self.MODEL:
            raise NotImplementedError

        obj = self.load(obj_dict)
        instance = self.MODEL(**obj.data)
        return instance
