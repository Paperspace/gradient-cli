import marshmallow

from . import BaseSchema
from .. import models


class MachineSchema(BaseSchema):
    MODEL = models.Machine

    machine_name = marshmallow.fields.Str(dump_to="machineName", load_from="machineName")
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
