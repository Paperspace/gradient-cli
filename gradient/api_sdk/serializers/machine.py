import marshmallow

from .base import BaseSchema
from .tag import TagSchema
from .. import models


class MachineEventSchema(BaseSchema):
    MODEL = models.MachineEvent

    name = marshmallow.fields.Str()
    state = marshmallow.fields.Str()
    created = marshmallow.fields.Str(dump_to="dtCreated", load_from="dtCreated")


class MachineSchema(BaseSchema):
    MODEL = models.Machine

    id = marshmallow.fields.Str(dump_to="machineId", load_from="machineId")
    name = marshmallow.fields.Str(dump_to="machineName", load_from="machineName")
    machine_type = marshmallow.fields.Str(dump_to="machineType", load_from="machineType")
    region = marshmallow.fields.Str()
    size = marshmallow.fields.Int()
    billing_type = marshmallow.fields.Str(dump_to="billingType", load_from="billingType")
    template_id = marshmallow.fields.Str(dump_to="templateId", load_from="templateId")
    assign_public_ip = marshmallow.fields.Bool(dump_to="assignPublicIp", load_from="assignPublicIp")
    dynamic_public_ip = marshmallow.fields.Bool(dump_to="dynamicPublicIp", load_from="dynamicPublicIp")
    network_id = marshmallow.fields.Str(dump_to="networkId", load_from="networkId")
    team_id = marshmallow.fields.Str(dump_to="teamId", load_from="teamId")
    user_id = marshmallow.fields.Str(dump_to="userId", load_from="userId")
    email = marshmallow.fields.Str()
    password = marshmallow.fields.Str()
    first_name = marshmallow.fields.Str(dump_to="firstName", load_from="firstName")
    last_name = marshmallow.fields.Str(dump_to="lastName", load_from="lastName")
    notification_email = marshmallow.fields.Str(dump_to="notificationEmail", load_from="notificationEmail")
    script_id = marshmallow.fields.Str(dump_to="scriptId", load_from="scriptId")
    os = marshmallow.fields.Str()
    cpus = marshmallow.fields.Int()
    ram = marshmallow.fields.Int()
    gpu = marshmallow.fields.Str()
    state = marshmallow.fields.Str()

    updates_pending = marshmallow.fields.Bool(dump_to="updatesPending", load_from="updatesPending")
    perform_auto_snapshot = marshmallow.fields.Bool(dump_to="performAutoSnapshot", load_from="performAutoSnapshot")
    auto_snapshot_frequency = marshmallow.fields.Str(dump_to="autoSnapshotFrequency", load_from="autoSnapshotFrequency")
    auto_snapshot_save_count = marshmallow.fields.Int(dump_to="autoSnapshotSaveCount",
                                                      load_from="autoSnapshotSaveCount")
    shutdown_timeout_in_hours = marshmallow.fields.Int(dump_to="shutdownTimeoutInHours",
                                                       load_from="shutdownTimeoutInHours")
    shutdown_timeout_forces = marshmallow.fields.Bool(dump_to="shutdownTimeoutForces",
                                                      load_from="shutdownTimeoutForces")
    agent_type = marshmallow.fields.Str(dump_to="agentType", load_from="agentType")
    storage_total = marshmallow.fields.Str(dump_to="storageTotal", load_from="storageTotal")
    storage_used = marshmallow.fields.Str(dump_to="storageUsed", load_from="storageUsed")
    public_ip_address = marshmallow.fields.Str(dump_to="publicIpAddress", load_from="publicIpAddress")
    private_ip_address = marshmallow.fields.Str(dump_to="privateIpAddress", load_from="privateIpAddress")
    usage_rate = marshmallow.fields.Str(dump_to="usageRate", load_from="usageRate")
    created_timestamp = marshmallow.fields.Str(dump_to="dtCreated", load_from="dtCreated")
    last_run_timestamp = marshmallow.fields.Str(dump_to="dtLastRun", load_from="dtLastRun")

    events = marshmallow.fields.Nested(MachineEventSchema, many=True)
    tags = marshmallow.fields.Nested(TagSchema, only="name", many=True, load_only=True)


class MachineSchemaForListing(MachineSchema):
    name = marshmallow.fields.Str()
