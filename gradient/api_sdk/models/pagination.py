from datetime import datetime

import attr


@attr.s
class Pagination(object):
    """
    Pagination class

    :param list[Any] data:
    :param str start_after:
    """
    data = attr.ib(type=list, default=None)
    start_after = attr.ib(type=str, default=None)