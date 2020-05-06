import datetime

import attr

from ..config import config
from ..utils import concatenate_urls


@attr.s
class Notebook(object):
    id = attr.ib(type=str, default=None)
    vm_type_id = attr.ib(type=int, default=None)
    container_id = attr.ib(type=int, default=None)
    container_name = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    cluster_id = attr.ib(type=int, default=None)
    registry_username = attr.ib(type=str, default=None)
    registry_password = attr.ib(type=str, default=None)
    default_entrypoint = attr.ib(type=str, default=None)
    container_user = attr.ib(type=str, default=None)
    shutdown_timeout = attr.ib(type=int, default=None)
    is_preemptible = attr.ib(type=bool, default=None)
    project_id = attr.ib(type=bool, default=None)
    state = attr.ib(type=bool, default=None)
    vm_type = attr.ib(type=bool, default=None)
    fqdn = attr.ib(type=bool, default=None)
    namespace = attr.ib(type=str, default=None)
    tags = attr.ib(type=list, factory=list)
    metrics_url = attr.ib(type=str, default=None)

    dt_created = attr.ib(type=datetime.datetime, default=None)
    dt_modified = attr.ib(type=datetime.datetime, default=None)
    dt_started = attr.ib(type=datetime.datetime, default=None)
    dt_stopped = attr.ib(type=datetime.datetime, default=None)
    dt_deleted = attr.ib(type=datetime.datetime, default=None)

    @property
    def url(self):
        url = concatenate_urls(config.WEB_URL, "/console/{}/notebook/{}".format(self.namespace, self.project_id))
        return url
