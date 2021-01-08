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

    def get(self, workflow_id):
        """Get a Workflow

        :param str workflow_id: Workflow ID [required]

        :returns: workflow
        :rtype: models.Workflow
        """
        repository = self.build_repository(repositories.GetWorkflow)
        return repository.get(id=workflow_id)
    

    def list_runs(self, workflow_id):
        """List workflows runs by workflow id

        :param str workflow_id: workflow ID

        :returns: list of workflow runs
        """

        repository = self.build_repository(repositories.ListWorkflowRuns)
        workflows_runs = repository.get(id=workflow_id)
        return workflows_runs

    def get_run(self, workflow_id, run):
        """List workflows runs by workflow id

        :param str workflow_id: workflow ID
        :param str run: run count

        :returns: list of workflow runs
        """

        repository = self.build_repository(repositories.GetWorkflowRun)
        workflows_runs = repository.get(id=workflow_id, run=run)
        return workflows_runs

