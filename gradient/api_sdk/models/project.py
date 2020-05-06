from datetime import datetime

import attr


@attr.s
class Project(object):
    """
    Project class

    :param str id:
    :param str name:
    :param str repository_name:
    :param str repository_url:
    :param datetime created:
    """
    id = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    repository_name = attr.ib(type=str, default=None)
    repository_url = attr.ib(type=str, default=None)
    created = attr.ib(type=datetime, default=None)
    tags = attr.ib(type=list, factory=list)
