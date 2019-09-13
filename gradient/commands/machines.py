import halo
import terminaltables

from gradient import api_sdk
from gradient.commands import common, BaseCommand


class GetMachinesClientMixin(object):
    def _get_client(self, api_key, logger):
        client = api_sdk.MachinesClient(api_key=api_key, logger=logger)
        return client


class CheckAvailabilityCommand(GetMachinesClientMixin, BaseCommand):
    def execute(self, machine_type, region):
        is_available = self.client.is_available(machine_type, region)
        self.logger.log("Machine available: {}".format(is_available))


class CreateMachineCommand(GetMachinesClientMixin, BaseCommand):
    def execute(self, kwargs):
        handle = self.client.create(**kwargs)
        self.logger.log("New machine created with id: {}".format(handle))


class UpdateMachineCommand(GetMachinesClientMixin, BaseCommand):
    def execute(self, machine_id, kwargs):
        self.client.update(machine_id, **kwargs)
        self.logger.log("Machine updated")


class StartMachineCommand(GetMachinesClientMixin, BaseCommand):
    def execute(self, id):
        self.client.start(id)
        self.logger.log("Machine started")


class StopMachineCommand(GetMachinesClientMixin, BaseCommand):
    def execute(self, id):
        self.client.stop(id)
        self.logger.log("Machine stopped")


class RestartMachineCommand(GetMachinesClientMixin, BaseCommand):
    def execute(self, id):
        self.client.restart(id)
        self.logger.log("Machine restarted")


class ShowMachineCommand(GetMachinesClientMixin, common.BaseCommand):
    WAITING_FOR_RESPONSE_MESSAGE = "Waiting for data..."

    def execute(self, id_):
        with halo.Halo(text=self.WAITING_FOR_RESPONSE_MESSAGE, spinner="dots"):
            instance = self._get_instance(id_)

        table_str = self._make_table(instance)
        self.logger.log(table_str)

    def _get_instance(self, id_):
        """
        :rtype: api_sdk.Machine
        """
        instance = self.client.get(id_)
        return instance

    def _make_table(self, machine):
        """
        :param api_sdk.Machine machine:
        """
        data = self._get_machine_table_data(machine)
        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string

    @staticmethod
    def _get_machine_table_data(machine):
        """
        :param api_sdk.Machine machine:
        """
        try:
            last_event = machine.events[-1]
            last_event_string = "name:     {}\nstate:    {}\ncreated:  {}" \
                .format(last_event.name, last_event.state, last_event.created)
        except (KeyError, IndexError):
            last_event_string = None

        data = (
            ("ID", machine.id),
            ("Name", machine.name),
            ("OS", machine.os),
            ("RAM", machine.ram),
            ("CPU", machine.cpus),
            ("GPU", machine.gpu),
            ("Storage Total", machine.storage_total),
            ("Storage Used", machine.storage_used),
            ("Usage Rate", machine.usage_rate),
            ("Shutdown Timeout In Hours", machine.shutdown_timeout_in_hours),
            ("Shutdown Timeout Forces", machine.shutdown_timeout_forces),
            ("Perform Auto Snapshot", machine.perform_auto_snapshot),
            ("Auto snapshot frequency", machine.auto_snapshot_frequency),
            ("Auto Snapshot Save Count", machine.auto_snapshot_save_count),
            ("Agent Type", machine.agent_type),
            ("Created", machine.created_timestamp),
            ("State", machine.state),
            ("Updates Pending", machine.updates_pending),
            ("Network ID", machine.network_id),
            ("Private IP Address", machine.private_ip_address),
            ("Public IP Address", machine.public_ip_address),
            ("Region", machine.region),
            ("Script ID", machine.script_id),
            ("Last Run", machine.last_run_timestamp),
            ("Dynamic Public IP", machine.dynamic_public_ip),
            ("Last event", last_event_string),
        )
        return data


class ListMachinesCommand(GetMachinesClientMixin, common.ListCommandMixin, BaseCommand):
    def _get_instances(self, kwargs):
        instances = self.client.list(**kwargs)
        return instances

    def _get_table_data(self, machines):
        """
        :param list[api_sdk.Machine] machines:
        :return:
        """
        data = [("ID", "Name", "OS", "CPU", "GPU", "RAM", "State", "Region")]
        for machine in machines:
            id_ = machine.id
            name = machine.name
            os_ = machine.os
            cpus = machine.cpus
            gpu = machine.gpu
            ram = machine.ram
            state = machine.state
            region = machine.region

            data.append((id_, name, os_, cpus, gpu, ram, state, region))

        return data

    def _get_request_json(self, kwargs):
        json_ = {"params": kwargs} if kwargs else None
        return json_


class DestroyMachineCommand(GetMachinesClientMixin, BaseCommand):
    def execute(self, machine_type, region):
        self.client.delete(machine_type, region)
        self.logger.log("Machine successfully destroyed")


class ShowMachineUtilizationCommand(GetMachinesClientMixin, BaseCommand):
    def execute(self, machine_id, billing_month):
        usage = self.client.get_utilization(machine_id, billing_month)
        table = self.make_details_table(usage)
        self.logger.log(table)

    @staticmethod
    def make_details_table(usage):
        data = (
            ("ID", usage.machine_id),
            ("Machine Seconds used", usage.machine_seconds_used),
            ("Machine Hourly rate", usage.machine_hourly_rate),
            ("Storage Seconds Used", usage.storage_seconds_used),
            ("Storage Monthly Rate", usage.storage_monthly_rate),
        )
        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string


class WaitForMachineStateCommand(GetMachinesClientMixin, BaseCommand):
    def execute(self, machine_id, state, interval=5):
        self.client.wait_for_state(machine_id, state, interval)
        self.logger.log("Machine state: {}".format(state))
