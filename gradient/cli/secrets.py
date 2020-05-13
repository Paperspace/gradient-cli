import click

from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.common import ClickGroup, api_key_option
from gradient.commands.secrets import DeleteSecretCommand, ListSecretsCommand, SetSecretCommand
from gradient.api_sdk.clients.secret_client import SECRET_ENTITIES


class EntityId(common.GradientOption):
    def handle_parse_result(self, ctx, opts, args):
        self.required = opts.get('entity') != 'team'
        return super(EntityId, self).handle_parse_result(ctx, opts, args)


@cli.group("secrets", help="Manage secrets", cls=ClickGroup)
def secrets():
    pass


@secrets.command("list", help="List secrets")
@click.argument("entity", type=click.Choice(SECRET_ENTITIES))
@click.option(
    "--id",
    "entity_id",
    help="Entity ID",
    cls=EntityId,
)
@api_key_option
@common.options_file
def get_secrets_list(api_key, entity, entity_id, options_file):
    command = ListSecretsCommand(api_key=api_key)
    command.execute(entity=entity, entity_id=entity_id)


@secrets.command("set", help="Set secret")
@click.argument("entity", type=click.Choice(SECRET_ENTITIES))
@click.option(
    "--id",
    "entity_id",
    help="Entity ID",
    cls=EntityId,
)
@click.option(
    "--name",
    "name",
    prompt=True,
    required=True,
    help="Secret name",
    cls=common.GradientOption,
)
@click.option(
    "--value",
    "value",
    hide_input=True,
    prompt=True,
    required=True,
    help="Secret value",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def set_secret(api_key, entity, entity_id, name, value, options_file):
    command = SetSecretCommand(api_key=api_key)
    command.execute(entity=entity, entity_id=entity_id, name=name, value=value)


@secrets.command("delete", help="Delete secret")
@click.argument("entity", type=click.Choice(SECRET_ENTITIES))
@click.option(
    "--id",
    "entity_id",
    help="Entity ID",
    cls=EntityId,
)
@click.option(
    "--name",
    "name",
    prompt=True,
    required=True,
    help="Secret name",
    cls=common.GradientOption,
)
@api_key_option
@common.options_file
def delete_secret(api_key, entity, entity_id, name, options_file):
    command = DeleteSecretCommand(api_key=api_key)
    command.execute(entity=entity, entity_id=entity_id, name=name)