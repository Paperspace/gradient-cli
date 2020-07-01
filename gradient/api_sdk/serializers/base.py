import marshmallow


class BaseSchema(marshmallow.Schema):
    MODEL = None

    @marshmallow.post_dump
    def remove_none_or_empty_values(self, data):
        return {
            key: value for key, value in data.items()
            if value not in (None, {}, [])
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
        if obj.data is None:
            return None

        instance = self.MODEL(**obj.data)
        self._get_nested(instance, obj_dict)
        return instance

    def _get_nested(self, instance, obj_dict):
        for field_name, field_type in self.fields.items():
            if not isinstance(field_type, marshmallow.fields.Nested):
                continue

            load_from = field_type.load_from or field_name
            field_dict = obj_dict.get(load_from, {})
            if field_dict is None:
                continue

            serializer = field_type.nested()
            field_data = serializer.get_instance(field_dict, many=field_type.many)

            if field_type.only:
                if isinstance(field_data, list):
                    field_data = [getattr(val, field_type.only) for val in field_data]
                else:
                    field_data = getattr(field_data, field_type.only)

            if field_data:
                setattr(instance, field_name, field_data)
