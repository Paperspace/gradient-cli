import attr


@attr.s
class Cluster(object):
    id = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    type = attr.ib(type=str, default=None)
