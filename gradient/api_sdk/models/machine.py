import attr


@attr.s
class Machine(object):
    machine_name = attr.ib(type=str, default=None)
    machine_type = attr.ib(type=str, default=None)
    region = attr.ib(type=str, default=None)
    size = attr.ib(type=int, default=None)
    billing_type = attr.ib(type=str, default=None)
    template_id = attr.ib(type=str, default=None)
    assign_public_ip = attr.ib(type=bool, default=None)
    dynamic_public_ip = attr.ib(type=str, default=None)
    network_id = attr.ib(type=str, default=None)
    team_id = attr.ib(type=str, default=None)
    user_id = attr.ib(type=str, default=None)
    email = attr.ib(type=str, default=None)
    password = attr.ib(type=str, default=None)
    first_name = attr.ib(type=str, default=None)
    last_name = attr.ib(type=str, default=None)
    notification_email = attr.ib(type=str, default=None)
    script_id = attr.ib(type=str, default=None)
