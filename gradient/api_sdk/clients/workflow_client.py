from .base_client import BaseClient
from .. import models, repositories
from ...exceptions import ReceivingDataFailedError


class WorkflowsClient(BaseClient):

    def create(self, name, project_id):
        """Create workflow with spec 

        :param str name: workflow name
        :param str project_id: project id

        :returns:  workflow create response
        :rtype: list[models.Workflow]
        """

        repository = self.build_repository(repositories.CreateWorkflow)
        workflow = repository.create(name=name, project_id=project_id)
        return workflow

    def run_workflow(self, spec, inputs, workflow_id, cluster_id=None):
        """Create workflow with spec 

        :param obj spec: workflow spec
        :param obj inputs: workflow inputs
        :param str workflow_id: workflow id
        :param str cluster_id: cluster id

        :returns:  workflow create response
        :rtype: list[models.Workflow]
        """

        repository = self.build_repository(repositories.CreateWorkflowRun)
        workflow = repository.create(spec=spec, inputs=inputs, id=workflow_id, cluster_id=cluster_id)
        return workflow

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

    def yield_logs(self, job_id, line=1, limit=10000):
        """Get log generator. Polls the API for new logs

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2

            job_logs_generator = job_client.yield_logs(
                job_id='Your_job_id_here',
                line=100,
                limit=100
            )

        :param str job_id:
        :param int line: line number at which logs starts to display on screen
        :param int limit: maximum lines displayed on screen, default set to 10 000

        :returns: generator yielding LogRow instances
        :rtype: Iterator[models.LogRow]
        """

        repository = self.build_repository(repositories.ListWorkflowLogs)
        logs = repository.yield_logs(id=job_id, line=line, limit=limit)
        return logs
    
    def logs(self, job_id, line=1, limit=10000):
        """Get log generator. Polls the API for new logs

        .. code-block:: python
            :linenos:
            :emphasize-lines: 2

            job_logs_generator = job_client.yield_logs(
                job_id='Your_job_id_here',
                line=100,
                limit=100
            )

        :param str job_id:
        :param int line: line number at which logs starts to display on screen
        :param int limit: maximum lines displayed on screen, default set to 10 000

        :returns: generator yielding LogRow instances
        :rtype: Iterator[models.LogRow]
        """

        repository = self.build_repository(repositories.ListWorkflowLogs)
        logs = repository.list(id=job_id, line=line, limit=limit)
        return logs