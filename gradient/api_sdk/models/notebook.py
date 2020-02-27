import attr

from gradient.api_sdk.config import config
from gradient.api_sdk.utils import urljoin


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

    @property
    def url(self):
        url = urljoin(config.WEB_URL, "/console/{}/notebook/{}".format(self.namespace, self.project_id))
        return url
