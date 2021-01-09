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
    required=True,
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
def create_workflow(ctx, api_key, workflow_id, cluster_id, spec_path, input_path, options_file):
    command = CreateWorkflowRunCommand(api_key=api_key)
    workflow_run = command.execute(spec_path=spec_path, input_path=input_path, workflow_id=workflow_id, cluster_id=cluster_id)
    ctx.invoke(list_logs, workflow_log_id=workflow_run['status']['logId'], line=1, limit=100, follow=True, api_key=api_key)


@workflows.command("list", help="List workflows")
@click.option(
    "--projectId",
    "project_id",
    required=False,
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
@api_key_option
@common.options_file
def get_workflow(api_key, workflow_id, options_file):
    command = GetWorkflowCommand(api_key=api_key)
    command.execute(workflow_id)


@workflows.command("runList", help="List workflow runs")
@click.option(
    "--id",
    "workflow_id",
    required=True,
    help="Workflow ID",
    cls=common.GradientOption,
)
@click.option(
    "--run",
    "run",
    prompt=False,
    required=False,
    help="Specify which run to get",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def get_workflows_runs(api_key, workflow_id, run, options_file):
    if run is None:
        command = ListWorkflowRunsCommand(api_key=api_key)
        command.execute(workflow_id=workflow_id)
    else:
        command = GetWorkflowRunCommand(api_key=api_key)
        command.execute(workflow_id=workflow_id, run=run)


@workflows.command("logs", help="List logs for specific workflow")
@click.option(
    "--id",
    "workflow_id",
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
@click.option(
    "--follow",
    "follow",
    required=False,
    default=False,
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def list_logs(api_key, workflow_id, workflow_log_id, line, limit, follow, options_file):
    command = WorkflowLogsCommand(api_key=api_key)
    if workflow_log_id:
        command.execute(workflow_log_id, line, limit, follow)
    else:
        command.execute(workflow_id, line, limit, follow)

