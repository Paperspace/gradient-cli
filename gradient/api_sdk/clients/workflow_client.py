from .base_client import BaseClient
from .. import models, repositories
from ...exceptions import ReceivingDataFailedError


class WorkflowsClient(BaseClient):

    def list(self, project_id):
        """List workflows by project

        :param str project_id: project ID

        :returns: list of workflows
        :rtype: list[models.Workflow]
        """

        repository = self.build_repository(repositories.ListWorkflows)
        workflows = repository.list(project_id=project_id)
        return workflows
    

    def list_runs(self, workflow_id):
        """List workflows runs by workflow id

        :param str workflow_id: workflow ID

        :returns: list of workflow runs
        :rtype: list[models.WorkflowRun]
        """

        repository = self.build_repository(repositories.ListWorkflowRuns)
        workflows = repository.list(workflow_id=workflow_id)
        return workflows

