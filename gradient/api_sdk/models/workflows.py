import datetime

import attr


@attr.s
class Workflow(object):
    id = attr.ib(type=str, default=None)
    team_id = attr.ib(type=int, default=None)
    project_id = attr.ib(type=int, default=None)
    name = attr.ib(type=str, default=None)
    workflow_spec_id = attr.ib(type=str, default=None)
    dt_deleted = attr.ib(type=datetime.datetime, default=None)
    dt_created = attr.ib(type=datetime.datetime, default=None)
    dt_modified = attr.ib(type=datetime.datetime, default=None)

@attr.s
class WorkflowSpec(object):
    id = attr.ib(type=str, default=None)
    data = attr.ib(type=str, default=None)
    hash_sha256 = attr.ib(type=str, default=None)
    dt_created = attr.ib(type=datetime.datetime, default=None)

@attr.s
class WorkflowRun(object):
    id = attr.ib(type=str, default=None)
    team_id = attr.ib(type=int, default=None)
    workflow_id = attr.ib(type=str, default=None)
    cluster_id = attr.ib(type=int, default=None)
    user_id = attr.ib(type=int, default=None)
    workflow_spec_id = attr.ib(type=str, default=None)
    seq_num = attr.ib(type=int, default=None)
    timeout = attr.ib(type=int, default=None)
    workflow_phase_id = attr.ib(type=int, default=None)
    name = attr.ib(type=str, default=None)
    message = attr.ib(type=str, default=None)
    dt_status = attr.ib(type=datetime.datetime, default=None)
    dt_started = attr.ib(type=datetime.datetime, default=None)
    dt_finished = attr.ib(type=datetime.datetime, default=None)
    dt_created = attr.ib(type=datetime.datetime, default=None)
    dt_modified = attr.ib(type=datetime.datetime, default=None)