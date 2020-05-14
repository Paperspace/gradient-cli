from .base_client import BaseClient, TagsSupportMixin
from .. import repositories, models
from ..repositories.machines import CheckMachineAvailability, DeleteMachine, ListMachines, WaitForState


class MachinesClient(TagsSupportMixin, BaseClient):
    entity = "machine"

    def create(
            self,
            name,
            machine_type,
            region,
            size,
            billing_type,
            template_id,
            assign_public_ip=None,
            dynamic_public_ip=None,
            network_id=None,
            team_id=None,
            user_id=None,
            email=None,
            password=None,
            first_name=None,
            last_name=None,
            notification_email=None,
            script_id=None,
            tags=None,
    ):
        """Create new machine

        :param str name: A memorable name for this machine [required]
        :param str machine_type: Machine type  [required]
        :param str region: Name of the region  [required]
        :param str size: Storage size for the machine in GB [required]
        :param str billing_type: Either 'monthly' or 'hourly' billing [required]
        :param str template_id: Template id of the template to use for creating this machine  [required]
        :param bool assign_public_ip: Assign a new public ip address. Cannot be used with dynamic_public_ip
        :param bool dynamic_public_ip: Temporarily assign a new public ip address on machine.
                                       Cannot be used with assign_public_ip
        :param str network_id: If creating on a specific network, specify its id
        :param str team_id: If creating the machine for a team, specify the team id
        :param str user_id: If assigning to an existing user other than yourself, specify the user id
                            (mutually exclusive with email, password, first_name, last_name)
        :param str email: If creating a new user for this machine, specify their email address
                          (mutually exclusive with user_id)
        :param str password: If creating a new user, specify their password (mutually exclusive with user_id)
        :param str first_name: If creating a new user, specify their first name (mutually exclusive with user_id)
        :param str last_name: If creating a new user, specify their last name (mutually exclusive with user_id)
        :param str notification_email: Send a notification to this email address when complete
        :param str script_id: The script id of a script to be run on startup
        :param list[str] tags: List of tags

        :returns: ID of created machine
        :rtype: str
        """

        instance = models.Machine(
            name=name,
            machine_type=machine_type,
            region=region,
            size=size,
            billing_type=billing_type,
            template_id=template_id,
            assign_public_ip=assign_public_ip,
            dynamic_public_ip=dynamic_public_ip,
            network_id=network_id,
            team_id=team_id,
            user_id=user_id,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            notification_email=notification_email,
            script_id=script_id,
        )

        repository = self.build_repository(repositories.CreateMachine)
        handle = repository.create(instance)
        if tags:
            self.add_tags(entity_id=handle, tags=tags)
        return handle

    def get(self, id):
        """Get machine instance

        :param str id: ID of a machine [required]

        :return: Machine instance
        :rtype: models.Machine
        """
        repository = self.build_repository(repositories.GetMachine)
        instance = repository.get(id=id)
        return instance

    def is_available(self, machine_type, region):
        """Check if specified machine is available in certain region

        :param str machine_type: Machine type  [required]
        :param str region: Name of the region  [required]

        :return: If specified machine is available in the region
        :rtype: bool
        """

        repository = self.build_repository(CheckMachineAvailability)
        handle = repository.get(machine_type=machine_type, region=region)
        return handle

    def restart(self, id):
        """Restart machine

        :param str id: ID of a machine [required]
        """

        repository = self.build_repository(repositories.RestartMachine)
        repository.restart(id)

    def start(self, id):
        """Start machine

        :param str id: ID of a machine [required]
        """

        repository = self.build_repository(repositories.StartMachine)
        repository.start(id)

    def stop(self, id):
        """Stop machine

        :param str id: ID of a machine [required]
        """

        repository = self.build_repository(repositories.StopMachine)
        repository.stop(id)

    def update(
            self,
            id,
            name=None,
            shutdown_timeout_in_hours=None,
            shutdown_timeout_forces=None,
            perform_auto_snapshot=None,
            auto_snapshot_frequency=None,
            auto_snapshot_save_count=None,
            dynamic_public_ip=None,
    ):
        """Update machine instance

        :param str id: Id of the machine to update  [required]
        :param str name: New name for the machine
        :param int shutdown_timeout_in_hours: Number of hours before machine is shutdown if no one is logged in
                                              via the Paperspace client
        :param bool shutdown_timeout_forces: Force shutdown at shutdown timeout, even if there is
                                             a Paperspace client connection
        :param bool perform_auto_snapshot: Perform auto snapshots
        :param str auto_snapshot_frequency: One of 'hour', 'day', 'week', or None
        :param int auto_snapshot_save_count: Number of snapshots to save
        :param str dynamic_public_ip: If true, assigns a new public ip address on machine start and releases it
                                      from the account on machine stop
        """
        instance = models.Machine(
            name=name,
            dynamic_public_ip=dynamic_public_ip,
            shutdown_timeout_in_hours=shutdown_timeout_in_hours,
            shutdown_timeout_forces=shutdown_timeout_forces,
            perform_auto_snapshot=perform_auto_snapshot,
            auto_snapshot_frequency=auto_snapshot_frequency,
            auto_snapshot_save_count=auto_snapshot_save_count,
        )

        repository = self.build_repository(repositories.UpdateMachine)
        repository.update(id, instance)

    def get_utilization(self, id, billing_month):
        """

        :param id: ID of the machine
        :param billing_month: Billing month in "YYYY-MM" format

        :return: Machine utilization info
        :rtype: models.MachineUtilization
        """
        repository = self.build_repository(repositories.GetMachineUtilization)
        usage = repository.get(id=id, billing_month=billing_month)
        return usage

    def delete(self, machine_id, release_public_ip=False):
        """Destroy machine with given ID

        :param str machine_id: ID of the machine
        :param bool release_public_ip: If the assigned public IP should be released
        """

        repository = self.build_repository(DeleteMachine)
        repository.delete(machine_id, release_public_ip=release_public_ip)

    def wait_for_state(self, machine_id, state, interval=5):
        """Wait for defined machine state

        :param str machine_id: ID of the machine
        :param str state: State of machine to wait for
        :param int interval: interval between polls
        """

        repository = self.build_repository(WaitForState)
        repository.wait_for_state(machine_id, state, interval)

    def list(
            self,
            id=None,
            name=None,
            os=None,
            ram=None,
            cpus=None,
            gpu=None,
            storage_total=None,
            storage_used=None,
            usage_rate=None,
            shutdown_timeout_in_hours=None,
            perform_auto_snapshot=None,
            auto_snapshot_frequency=None,
            auto_snapshot_save_count=None,
            agent_type=None,
            created_timestamp=None,
            state=None,
            updates_pending=None,
            network_id=None,
            private_ip_address=None,
            public_ip_address=None,
            region=None,
            user_id=None,
            team_id=None,
            last_run_timestamp=None,
    ):
        """

        :param str id: Optional machine id to match on
        :param str name: Filter by machine name
        :param str os: Filter by os used
        :param int ram: Filter by machine RAM (in bytes)
        :param int cpus: Filter by CPU count
        :param str gpu: Filter by GPU type
        :param str storage_total: Filter by total storage
        :param str storage_used: Filter by storage used
        :param str usage_rate: Filter by usage rate
        :param int shutdown_timeout_in_hours: Filter by shutdown timeout
        :param bool perform_auto_snapshot: Filter by performAutoSnapshot flag
        :param str auto_snapshot_frequency: Filter by autoSnapshotFrequency flag
        :param int auto_snapshot_save_count: Filter by auto shapshots count
        :param str agent_type: Filter by agent type
        :param datetime created_timestamp: Filter by date created
        :param str state: Filter by state
        :param str updates_pending: Filter by updates pending
        :param str network_id: Filter by network ID
        :param str private_ip_address: Filter by private IP address
        :param str public_ip_address: Filter by public IP address
        :param str region: Filter by region. One of {CA, NY2, AMS1}
        :param str user_id: Filter by user ID
        :param str team_id: Filter by team ID
        :param str last_run_timestamp: Filter by last run date

        :return: List of machines
        :rtype: list[models.Machine]
        """

        repository = self.build_repository(ListMachines)
        machines = repository.list(
            id=id,
            name=name,
            os=os,
            ram=ram,
            cpus=cpus,
            gpu=gpu,
            storage_total=storage_total,
            storage_used=storage_used,
            usage_rate=usage_rate,
            shutdown_timeout_in_hours=shutdown_timeout_in_hours,
            perform_auto_snapshot=perform_auto_snapshot,
            auto_snapshot_frequency=auto_snapshot_frequency,
            auto_snapshot_save_count=auto_snapshot_save_count,
            agent_type=agent_type,
            created_timestamp=created_timestamp,
            state=state,
            updates_pending=updates_pending,
            network_id=network_id,
            private_ip_address=private_ip_address,
            public_ip_address=public_ip_address,
            region=region,
            user_id=user_id,
            team_id=team_id,
            last_run_timestamp=last_run_timestamp,
        )
        return machines
