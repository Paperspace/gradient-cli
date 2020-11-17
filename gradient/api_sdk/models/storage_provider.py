import attr


@attr.s
class StorageProvider(object):
    """
    Storage provider class
    """
    id = attr.ib(type=str, default=None)
    type = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    config = attr.ib(type=dict, factory=dict)
