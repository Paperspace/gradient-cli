import click

from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.common import ClickGroup, api_key_option
from gradient.commands.workflows import ListWorkflowsCommand, ListWorkflowRunsCommand, GetWorkflowCommand, GetWorkflowRunCommand, CreateWorkflowCommand, CreateWorkflowRunCommand, WorkflowLogsCommand


@cli.group("workflows", help="Manage workflows", cls=ClickGroup)
def workflows():
    pass

@workflows.command("create", help="Create workflow")
@click.option(
    "--name",
    "name",
    required=True,
    help="Workflow name",
    cls=common.GradientOption,
)
@click.option(
    "--projectId",
    "project_id",
    required=True,
    help="Workflow name",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def create_workflow(api_key, name, project_id, options_file):
    command = CreateWorkflowCommand(api_key=api_key)
    command.execute(name=name, project_id=project_id)


@workflows.command("run", help="Run workflow spec")
@click.option(
    "--id",
    "workflow_id",
    required=True,
    help="Workflow ID",
    cls=common.GradientOption,
)
@click.option(
    "--clusterId",
    "cluster_id",
    required=False,
    help="Cluster ID",
    cls=common.GradientOption,
)
@click.option(
    "--path",
    "spec_path",
    required=True,
    help="Path to spec",
    cls=common.GradientOption,
)
@click.option(
    "--inputPath",
    "input_path",
    required=False,
    help="Path to inputs",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
@click.pass_context
def create_workflow_run(ctx, api_key, workflow_id, cluster_id, spec_path, input_path, options_file):
    command = CreateWorkflowRunCommand(api_key=api_key)
    workflow_run = command.execute(spec_path=spec_path, input_path=input_path, workflow_id=workflow_id, cluster_id=cluster_id)
    try:
        logId = workflow_run['status']['logId']
        # disable broken workflow-logs until we implement a functional job-specific or job-concatted log system
        # ctx.invoke(list_logs, workflow_log_id=logId, line=1, limit=100, follow=True, api_key=api_key)
    except KeyError:
        pass


@workflows.command("list", help="List workflows")
@click.option(
    "--projectId",
    "project_id",
    required=True,
    help="Project ID",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def get_workflows_list(api_key, project_id, options_file):
    command = ListWorkflowsCommand(api_key=api_key)
    command.execute(project_id=project_id)


@workflows.command("get", help="Get workflow info")
@click.option(
    "--id",
    "workflow_id",
    required=True,
    cls=common.GradientOption,
    help="Workflow Id",
)
@click.option(
    "--show-runs",
    "show_runs",
    prompt=False,
    required=False,
    is_flag=True,
    default=False,
    help="Fetch runs",
    cls=common.GradientOption,
)
@click.option(
    "--run",
    "run",
    prompt=False,
    required=False,
    help="Specify workload run",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def get_workflow(api_key, workflow_id, show_runs, run, options_file):
    if show_runs:
        if run is None:
            command = ListWorkflowRunsCommand(api_key=api_key)
            command.execute(workflow_id=workflow_id)
        else:
            command = GetWorkflowRunCommand(api_key=api_key)
            command.execute(workflow_id=workflow_id, run=run)
    else:
        command = GetWorkflowCommand(api_key=api_key)
        command.execute(workflow_id)



@workflows.command("logs", help="List logs for specific workflow")
@click.option(
    "--id",
    "workflow_id",
    help="Workflow ID",
    required=True,
    cls=common.GradientOption,
)
@click.option(
    "--run",
    "run",
    help="Specify workload run",
    required=True,
    cls=common.GradientOption,
)
@click.option(
    "--logId",
    "workflow_log_id",
    required=False,
    cls=common.GradientOption,
)
@click.option(
    "--line",
    "line",
    required=False,
    default=0,
    cls=common.GradientOption,
)
@click.option(
    "--limit",
    "limit",
    required=False,
    default=10000,
    cls=common.GradientOption,
)
# TODO (roger): Disabled follow for now since we iterate through multiple workflow job ids 
# instead of the top level workflow id
# @click.option(
#     "--follow",
#     "follow",
#     required=False,
#     default=False,
#     cls=common.GradientOption,
# )
@api_key_option
@common.options_file
@click.pass_context
def list_logs(ctx, api_key, workflow_id, workflow_log_id, run, line, limit, options_file, follow=False):
    command = WorkflowLogsCommand(api_key=api_key)
    if workflow_log_id:
        command.execute(workflow_log_id, line, limit, follow)
    else:
        getRunCommand = GetWorkflowRunCommand(api_key=api_key)
        workflow_run = getRunCommand.get_instance(workflow_id, run)
        try:
            jobs = workflow_run['status']['jobs']
            for job_name, job in jobs.items():
                logId = job['logId']
                click.echo(f'Job Name: {job_name}')
                command.execute(logId, line, limit, follow)
        except KeyError:
            pass

