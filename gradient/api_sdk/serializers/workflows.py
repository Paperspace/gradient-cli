import marshmallow as ma

from .base import BaseSchema
from .. import models


class WorkflowSchema(BaseSchema):
    MODEL = models.Workflow

    id = ma.fields.Str(dump_to="id", load_from="id")
    team_id = ma.fields.Str(dump_to="teamId", load_from="teamId")
    project_id = ma.fields.Int(required=True, dump_to="projectId", load_from="projectId")
    name = ma.fields.Str(dump_to="name", load_from="name")
    workflow_spec_id = ma.fields.Str(dump_to="workflowSpecId", load_from="workflowSpecId")
    dt_deleted = ma.fields.DateTime(dump_to="dtDeleted", load_from="dtDeleted")
    dt_created = ma.fields.DateTime(dump_to="dtCreated", load_from="dtCreated")
    dt_modified = ma.fields.DateTime(dump_to="dtModified", load_from="dtModified")


class WorkflowSpecSchema(BaseSchema):
    MODEL = models.WorkflowSpec

    id = ma.fields.Str(dump_to="id", load_from="id")
    data = ma.fields.Str(dump_to="data", load_from="data")
    hash_sha256 = ma.fields.Str(dump_to="hashSha256", load_from="hashSha256")
    dt_created = ma.fields.DateTime(dump_to="dtCreated", load_from="dtCreated")


class WorkflowRunSchema(BaseSchema):
    MODEL = models.WorkflowRun

    id = ma.fields.Str(dump_to="id", load_from="id")
    team_id = ma.fields.Int(dump_to="teamId", load_from="teamId")
    workflow_id = ma.fields.Str(dump_to="workflowId", load_from="workflowId")
    cluster_id = ma.fields.Int(required=True, dump_to="clusterId", load_from="clusterId")
    user_id = ma.fields.Int(required=True, dump_to="userId", load_from="userId")
    workflow_spec_id = ma.fields.Str(dump_to="workflowSpecId", load_from="workflowSpecId")
    seq_num = ma.fields.Int(required=True, dump_to="seqNum", load_from="seqNum")
    timeout = ma.fields.Int(required=True, dump_to="timeout", load_from="timeout")
    workflow_phase_id = ma.fields.Int(required=True, dump_to="workflowPhaseId", load_from="workflowPhaseId")
    name = ma.fields.Str(dump_to="name", load_from="name")
    message = ma.fields.Str(dump_to="message", load_from="message")
    dt_status = ma.fields.DateTime(dump_to="dtStatus", load_from="dtStatus")
    dt_started = ma.fields.DateTime(dump_to="dtStarted", load_from="dtStarted")
    dt_finished = ma.fields.DateTime(dump_to="dtFinished", load_from="dtFinished")
    dt_created = ma.fields.DateTime(dump_to="dtCreated", load_from="dtCreated")
    dt_modified = ma.fields.DateTime(dump_to="dtModified", load_from="dtDeleted")
