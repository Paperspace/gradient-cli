import datetime

import attr

from ..config import config
from ..utils import concatenate_urls


@attr.s
class Notebook(object):
    id = attr.ib(type=str, default=None)
    machine_type = attr.ib(type=str, default=None)
    vm_type_id = attr.ib(type=int, default=None)
    vm_type_label = attr.ib(type=str, default=None)
    container_id = attr.ib(type=int, default=None)
    container_name = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    cluster_id = attr.ib(type=str, default=None)
    registry_username = attr.ib(type=str, default=None)
    registry_password = attr.ib(type=str, default=None)
    command = attr.ib(type=str, default=None)
    default_entrypoint = attr.ib(type=str, default=None)
    container_user = attr.ib(type=str, default=None)
    shutdown_timeout = attr.ib(type=int, default=None)
    is_preemptible = attr.ib(type=bool, default=None)
    project_id = attr.ib(type=str, default=None)
    project_handle = attr.ib(type=str, default=None)
    state = attr.ib(type=str, default=None)
    vm_type = attr.ib(type=str, default=None)
    fqdn = attr.ib(type=str, default=None)
    namespace = attr.ib(type=str, default=None)
    tags = attr.ib(type=list, factory=list)
    metrics_url = attr.ib(type=str, default=None)
    is_public = attr.ib(type=str, default=None)
    token = attr.ib(type=str, default=None)
    job_error = attr.ib(type=str, default=None)
    job_handle = attr.ib(type=str, default=None)
    container = attr.ib(type=str, default=None)
    container_url = attr.ib(type=str, default=None)
    base_container = attr.ib(type=str, default=None)
    base_container_url = attr.ib(type=str, default=None)
    environment = attr.ib(type=dict, default=None)
    workspace = attr.ib(type=str, default=None)
    workspace_username = attr.ib(type=str, default=None)
    workspace_password = attr.ib(type=str, default=None)
    workspace_ref = attr.ib(type=str, default=None)
    should_run_on_create = attr.ib(type=str, default=None)

    dt_created = attr.ib(type=datetime.datetime, default=None)
    dt_modified = attr.ib(type=datetime.datetime, default=None)
    dt_provisioning_started = attr.ib(type=datetime.datetime, default=None)
    dt_provisioning_finished = attr.ib(type=datetime.datetime, default=None)
    dt_started = attr.ib(type=datetime.datetime, default=None)
    dt_finished = attr.ib(type=datetime.datetime, default=None)
    dt_teardown_started = attr.ib(type=datetime.datetime, default=None)
    dt_teardown_finished = attr.ib(type=datetime.datetime, default=None)
    dt_workspace_upload_finished = attr.ib(type=datetime.datetime, default=None)
    dt_deleted = attr.ib(type=datetime.datetime, default=None)

    @property
    def url(self):
        url = concatenate_urls(config.WEB_URL, "/{}/notebook/{}".format(self.namespace, self.project_handle))
        return url


@attr.s
class NotebookStart(object):
    notebook_id = attr.ib(type=str, default=None)
    machine_type = attr.ib(type=str, default=None)
    vm_type_id = attr.ib(type=int, default=None)
    vm_type_label = attr.ib(type=str, default=None)
    cluster_id = attr.ib(type=str, default=None)
    shutdown_timeout = attr.ib(type=int, default=None)
    is_preemptible = attr.ib(type=bool, default=None)
    notebook_name = attr.ib(type=str, default=None)

