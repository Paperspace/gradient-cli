import attr


@attr.s
class Dataset(object):
    url = attr.ib(type=str, default=None)
    tag = attr.ib(type=str, default=None)
    auth = attr.ib(type=str, default=None)
