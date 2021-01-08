import click

from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.common import ClickGroup, api_key_option
from gradient.commands.workflows import ListWorkflowsCommand, ListWorkflowRunsCommand, GetWorkflowCommand, GetWorkflowRunCommand


@cli.group("workflows", help="Manage workflows", cls=ClickGroup)
def workflows():
    pass

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
    prompt=True,
    required=True,
    cls=common.GradientOption,
    help="Workflow Id",
)
@api_key_option
@common.options_file
def get_artifacts(api_key, workflow_id, options_file):
    command = GetWorkflowCommand(api_key=api_key)
    command.execute(workflow_id)


@workflows.command("runs", help="List workflow runs")
@click.option(
    "--workflowId",
    "workflow_id",
    prompt=True,
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


