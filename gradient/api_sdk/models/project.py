import attr


@attr.s
class Project(object):
    id = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    repository_name = attr.ib(type=str, default=None)
    repository_url = attr.ib(type=str, default=None)
