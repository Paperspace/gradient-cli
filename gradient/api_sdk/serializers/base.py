import marshmallow


class BaseSchema(marshmallow.Schema):
    MODEL = None

    @marshmallow.post_dump
    def remove_none_values(self, data):
        return {
            key: value for key, value in data.items()
            if value not in (None, {})
        }

    def get_instance(self, obj_dict, many=False):
        if not self.MODEL:
            raise NotImplementedError
        if not many:
            return self._get_instance(obj_dict)

        instances = [self._get_instance(obj_d) for obj_d in obj_dict]
        return instances

    def _get_instance(self, obj_dict):
        obj = self.load(obj_dict)
        instance = self.MODEL(**obj.data)
        return instance
