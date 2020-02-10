from .. import logger as sdk_logger
from ..repositories.clusters import ValidateClusterRepository
from gradient.api_sdk.sdk_exceptions import GradientSdkError


class BaseClient(object):
    def __init__(
            self, api_key,
            logger=sdk_logger.MuteLogger()
    ):
        """
        Base class. All client classes inherit from it.

        An API key can be created at paperspace.com after you sign in to your account. After obtaining it, you can set
        it in the CLI using the command::

            gradient apiKey XXXXXXXXXXXXXXXXXXX

        or you can provide your API key in any command, for example::

            gradient experiments run ... --apiKey XXXXXXXXXXXXXXXXXXX

        :param str api_key: your API key
        :param sdk_logger.Logger logger:
        """
        self.api_key = api_key
        self.logger = logger

    CLUSTER_VPC_TYPE = "Kubernetes Processing Site"

    def validate_cluster_id_need_vpc(self, cluster_id, use_vpc):
        if cluster_id and not use_vpc:
            cluster_repo = ValidateClusterRepository(api_key=self.api_key, logger=self.logger)
            cluster_details = cluster_repo.get(cluster_id=cluster_id)
            if cluster_details.get("type") == self.CLUSTER_VPC_TYPE:
                raise GradientSdkError("Provided cluster id need --vpc flag to proceed")
