from gradient.api_sdk import repositories, models
from gradient.api_sdk.repositories.machines import CheckMachineAvailability
from .base_client import BaseClient


class MachinesClient(BaseClient):
    def create(
            self,
            machine_name,
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
    ):
        """Create new machine

        :param str machine_name: A memorable name for this machine [required]
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

        :returns: ID of created machine
        :rtype: str
        """

        instance = models.Machine(
            machine_name=machine_name,
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

        repository = repositories.CreateMachine(api_key=self.api_key, logger=self.logger)
        handle = repository.create(instance)
        return handle

    def is_available(self, machine_type, region):
        """Check if specified machine is available in certain region

        :param str machine_type: Machine type  [required]
        :param str region: Name of the region  [required]

        :return: If specified machine is available in the region
        :rtype: bool
        s"""

        repository = CheckMachineAvailability(self.api_key, self.logger)
        handle = repository.get(machine_type=machine_type, region=region)
        return handle
