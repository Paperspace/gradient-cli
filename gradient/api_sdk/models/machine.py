import attr


@attr.s
class Machine(object):
    id = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
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
    os = attr.ib(type=str, default=None)
    cpus = attr.ib(type=str, default=None)
    ram = attr.ib(type=int, default=None)
    gpu = attr.ib(type=str, default=None)
    state = attr.ib(type=str, default=None)
    updates_pending = attr.ib(type=bool, default=None)
    perform_auto_snapshot = attr.ib(type=str, default=None)
    auto_snapshot_frequency = attr.ib(type=str, default=None)
    auto_snapshot_save_count = attr.ib(type=int, default=None)
    shutdown_timeout_in_hours = attr.ib(type=str, default=None)
    shutdown_timeout_forces = attr.ib(type=bool, default=None)
    agent_type = attr.ib(type=str, default=None)
    storage_total = attr.ib(type=str, default=None)
    storage_used = attr.ib(type=str, default=None)
    public_ip_address = attr.ib(type=str, default=None)
    private_ip_address = attr.ib(type=int, default=None)
    usage_rate = attr.ib(type=int, default=None)
    created_timestamp = attr.ib(type=str, default=None)
    last_run_timestamp = attr.ib(type=str, default=None)
    events = attr.ib(type=list, default=None)
    tags = attr.ib(type=list, factory=list)


@attr.s
class MachineEvent(object):
    name = attr.ib(type=str, default=None)
    state = attr.ib(type=str, default=None)
    created = attr.ib(type=str, default=None)


@attr.s
class MachineUtilization(object):
    machine_id = attr.ib(type=str, default=None)
    machine_seconds_used = attr.ib(type=float, default=None)
    machine_billing_month = attr.ib(type=str, default=None)
    machine_hourly_rate = attr.ib(type=str, default=None)
    storage_seconds_used = attr.ib(type=float, default=None)
    storage_billing_month = attr.ib(type=str, default=None)
    storage_monthly_rate = attr.ib(type=str, default=None)
