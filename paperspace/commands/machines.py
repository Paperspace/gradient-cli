import pydoc
import time

import terminaltables

from paperspace import logger
from paperspace.exceptions import BadResponse
from paperspace.utils import get_terminal_lines


class CommandBase(object):
    def __init__(self, api=None, logger_=logger):
        self.api = api
        self.logger = logger_

    def _log_message(self, response, success_msg_template, error_msg):
        if response.ok:
            try:
                handle = response.json()
            except (ValueError, KeyError):
                self.logger.log(success_msg_template)
            else:
                msg = success_msg_template.format(**handle)
                self.logger.log(msg)
        else:
            try:
                data = response.json()
                self.logger.log_error_response(data)
            except ValueError:
                self.logger.log(error_msg)


class CheckAvailabilityCommand(CommandBase):
    def execute(self, region, machine_type):
        params = {"region": region,
                  "machineType": machine_type}
        response = self.api.get("machines/getAvailability/", params=params)
        self._log_message(response,
                          "Machine available: {available}",
                          "Unknown error while checking machine availability")


class CreateMachineCommand(CommandBase):
    def execute(self, kwargs):
        response = self.api.post("/machines/createSingleMachinePublic/", json=kwargs)
        self._log_message(response,
                          "New machine created with id: {id}",
                          "Unknown error while creating machine")


class UpdateMachineCommand(CommandBase):
    def execute(self, machine_id, kwargs):
        url = "/machines/{}/updateMachinePublic/".format(machine_id)
        response = self.api.post(url, json=kwargs)
        self._log_message(response,
                          "Machine updated",
                          "Unknown error while updating machine")


class StartMachineCommand(CommandBase):
    def execute(self, machine_id):
        url = "/machines/{}/start/".format(machine_id)
        response = self.api.post(url)
        self._log_message(response,
                          "Machine started",
                          "Unknown error while starting the machine")


class StopMachineCommand(CommandBase):
    def execute(self, machine_id):
        url = "/machines/{}/stop/".format(machine_id)
        response = self.api.post(url)
        self._log_message(response,
                          "Machine stopped",
                          "Unknown error while stopping the machine")


class RestartMachineCommand(CommandBase):
    def execute(self, machine_id):
        url = "/machines/{}/restart/".format(machine_id)
        response = self.api.post(url)
        self._log_message(response,
                          "Machine restarted",
                          "Unknown error while restarting the machine")


class ShowMachineCommand(CommandBase):
    def execute(self, machine_id):
        params = {"machineId": machine_id}
        response = self.api.get("/machines/getMachinePublic/", params=params)

        try:
            data = response.json()
            if not response.ok:
                self.logger.log_error_response(data)
                return
        except (ValueError, KeyError) as e:
            self.logger.log("Error while parsing response data: {}".format(e))
        else:
            table = self.make_details_table(data)
            self.logger.log(table)

    @staticmethod
    def make_details_table(machine):
        try:
            last_event = machine["events"][-1]
            last_event_string = "name:     {}\nstate:    {}\ncreated:  {}" \
                .format(last_event.get("name"), last_event.get("state"), last_event.get("created"))
        except (KeyError, IndexError):
            last_event_string = None

        data = (
            ("ID", machine.get("id")),
            ("Name", machine.get("name")),
            ("OS", machine.get("os")),
            ("RAM", machine.get("ram")),
            ("CPU", machine.get("cpus")),
            ("GPU", machine.get("gpu")),
            ("Storage Total", machine.get("storageTotal")),
            ("Storage Used", machine.get("storageUsed")),
            ("Usage Rate", machine.get("usageRate")),
            ("Shutdown Timeout In Hours", machine.get("shutdownTimeoutInHours")),
            ("Shutdown Timeout Forces", machine.get("shutdownTimeoutForces")),
            ("Perform Auto Snapshot", machine.get("performAutoSnapshot")),
            ("Auto snapshot frequency", machine.get("autoSnapshotFrequency")),
            ("Auto Snapshot Save Count", machine.get("autoSnapshotSaveCount")),
            ("Agent Type", machine.get("agentType")),
            ("Created", machine.get("dtCreated")),
            ("State", machine.get("state")),
            ("Updates Pending", machine.get("updatesPending")),
            ("Network ID", machine.get("networkId")),
            ("Private IP Address", machine.get("privateIpAddress")),
            ("Public IP Address", machine.get("publicIpAddress")),
            ("Region", machine.get("region")),
            ("Script ID", machine.get("scriptId")),
            ("Last Run", machine.get("dtLastRun")),
            ("Dynamic Public IP", machine.get("dynamicPublicIp")),
            ("Last event", last_event_string),
        )
        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string


class ListMachinesCommand(CommandBase):
    def execute(self, kwargs):
        json_ = {"params": kwargs} if kwargs else None
        response = self.api.get("/machines/getMachines/", json=json_)

        try:
            data = response.json()
            if not response.ok:
                self.logger.log_error_response(data)
                return
        except (ValueError, KeyError) as e:
            self.logger.log("Error while parsing response data: {}".format(e))
        else:
            self._log_machines_list(data)

    def _log_machines_list(self, machines):
        if not machines:
            self.logger.log("No machines found")
        else:
            table_str = self._make_machines_list_table(machines)
            if len(table_str.splitlines()) > get_terminal_lines():
                pydoc.pager(table_str)
            else:
                self.logger.log(table_str)

    @staticmethod
    def _make_machines_list_table(machines):
        data = [("ID", "Name", "OS", "CPU", "GPU", "RAM", "State", "Region")]
        for machine in machines:
            id_ = machine.get("id")
            name = machine.get("name")
            os_ = machine.get("os")
            cpus = machine.get("cpus")
            gpu = machine.get("gpu")
            ram = machine.get("ram")
            state = machine.get("state")
            region = machine.get("region")
            data.append((id_, name, os_, cpus, gpu, ram, state, region))

        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string


class DestroyMachineCommand(CommandBase):
    def execute(self, machine_id, release_public_ip):
        json_ = {"releasePublicIp": release_public_ip} if release_public_ip else None
        url = "/machines/{}/destroyMachine/".format(machine_id)
        response = self.api.post(url, json=json_)
        self._log_message(response,
                          "Machine successfully destroyed",
                          "Unknown error while destroying the machine")


class ShowMachineUtilisationCommand(CommandBase):
    def execute(self, machine_id, billing_month):
        params = {"machineId": machine_id,
                  "billingMonth": billing_month}
        response = self.api.get("machines/getUtilization/", params=params)

        try:
            data = response.json()
            if not response.ok:
                self.logger.log_error_response(data)
                return
        except (ValueError, KeyError) as e:
            self.logger.log("Error while parsing response data: {}".format(e))
        else:
            table = self.make_details_table(data)
            self.logger.log(table)

    @staticmethod
    def make_details_table(machine):
        data = (
            ("ID", machine.get("machineId")),
            ("Machine Seconds used", machine["utilization"].get("secondsUsed")),
            ("Machine Hourly rate", machine["utilization"].get("hourlyRate")),
            ("Storage Seconds Used", machine["storageUtilization"].get("secondsUsed")),
            ("Storage Monthly Rate", machine["storageUtilization"].get("monthlyRate")),
        )
        ascii_table = terminaltables.AsciiTable(data)
        table_string = ascii_table.table
        return table_string


class WaitForMachineStateCommand(CommandBase):
    def execute(self, machine_id, state, interval=5):
        while True:
            try:
                current_state = self._get_machine_state(machine_id)
            except BadResponse as e:
                self.logger.log(e)
                return
            else:
                if current_state == state:
                    break

            time.sleep(interval)

        self.logger.log("Machine state: {}".format(current_state))

    def _get_machine_state(self, machine_id):
        params = {"machineId": machine_id}
        response = self.api.get("/machines/getMachinePublic/", params=params)
        try:
            json_ = response.json()
            if not response.ok:
                self.logger.log_error_response(json_)
                raise BadResponse("Error while reading machine state")
            state = json_.get("state")
        except (ValueError, AttributeError):
            raise BadResponse("Unknown error while reading machine state")
        return state
