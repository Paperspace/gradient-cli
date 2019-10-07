import attr


@attr.s
class Artifact(object):
    file = attr.ib(type=str)
    url = attr.ib(type=str, default=None)
    size = attr.ib(type=int, default=None)
