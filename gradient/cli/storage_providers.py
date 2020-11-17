import click

from gradient.cli import common
from gradient.cli.cli import cli
from gradient.cli.common import ClickGroup, api_key_option
from gradient.commands import storage_providers as commands


@cli.group("storageProviders", help="Manage storage providers", cls=ClickGroup)
def storage_providers():
    pass


@storage_providers.group("create", help="Create storage providers", cls=ClickGroup)
def create():
    pass


@storage_providers.group("update", help="Update storage providers", cls=ClickGroup)
def update():
    pass


@storage_providers.command("list", help="List storage providers")
@api_key_option
@common.options_file
def get_storage_providers_list(api_key, options_file):
    command = commands.ListStorageProvidersCommand(api_key=api_key)
    for has_more in command.execute():
        if has_more:
            click.echo("")
            click.confirm("Do you want to continue?", abort=True)
            click.echo("")


@storage_providers.command("details", help="Show storage provider details")
@click.option(
    "--id",
    "id",
    help="Storage provider ID",
    cls=common.GradientOption,
    required=True,
)
@common.api_key_option
@common.options_file
def show_storage_provider(id, api_key, options_file):
    command = commands.ShowStorageProviderDetailsCommand(api_key=api_key)
    command.execute(id)


@create.command("s3", help="Create S3 storage provider")
@click.option(
    "--name",
    "name",
    help="Storage provider name",
    cls=common.GradientOption,
    required=True,
)
@click.option(
    "--bucket",
    "bucket",
    help="S3 bucket",
    cls=common.GradientOption,
    required=True,
)
@click.option(
    "--accessKey",
    "access_key",
    help="S3 access key ID",
    cls=common.GradientOption,
    required=True,
)
@click.option(
    "--secretAccessKey",
    "secret_access_key",
    help="S3 secret access key",
    cls=common.GradientOption,
    required=True,
)
@click.option(
    "--endpoint",
    "endpoint",
    help="S3 endpoint URL",
    cls=common.GradientOption,
)
@click.option(
    "--region",
    "region",
    help="S3 region",
    cls=common.GradientOption,
)
@click.option(
    "--signatureVersion",
    "signature_version",
    help="S3 signature version (ex: v4)",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def create_s3_storage_provider(
        name,
        bucket,
        access_key,
        secret_access_key,
        endpoint,
        region,
        signature_version,
        api_key,
        options_file,
):
    command = commands.CreateS3StorageProviderCommand(api_key=api_key)
    command.execute(
        name=name,
        bucket=bucket,
        access_key=access_key,
        secret_access_key=secret_access_key,
        endpoint=endpoint,
        region=region,
        signature_version=signature_version,
    )


@update.command("s3", help="Update S3 storage provider")
@click.option(
    "--id",
    "id",
    help="Storage provider ID",
    cls=common.GradientOption,
    required=True,
)
@click.option(
    "--name",
    "name",
    help="Storage provider name",
    cls=common.GradientOption,
)
@click.option(
    "--bucket",
    "bucket",
    help="S3 bucket",
    cls=common.GradientOption,
)
@click.option(
    "--accessKey",
    "access_key",
    help="S3 access key ID",
    cls=common.GradientOption,
)
@click.option(
    "--secretAccessKey",
    "secret_access_key",
    help="S3 secret access key",
    cls=common.GradientOption,
)
@click.option(
    "--endpoint",
    "endpoint",
    help="S3 endpoint URL",
    cls=common.GradientOption,
)
@click.option(
    "--region",
    "region",
    help="S3 region",
    cls=common.GradientOption,
)
@click.option(
    "--signatureVersion",
    "signature_version",
    help="S3 signature version (ex: v4)",
    cls=common.GradientOption,
)
@common.api_key_option
@common.options_file
def update_s3_storage_provider(
        id,
        name,
        bucket,
        access_key,
        secret_access_key,
        endpoint,
        region,
        signature_version,
        api_key,
        options_file,
):
    command = commands.UpdateS3StorageProviderCommand(api_key=api_key)
    command.execute(
        storage_provider_id=id,
        name=name,
        bucket=bucket,
        access_key=access_key,
        secret_access_key=secret_access_key,
        endpoint=endpoint,
        region=region,
        signature_version=signature_version,
    )


@storage_providers.command("delete", help="Delete storage provider")
@click.option(
    "--id",
    "id",
    help="Storage provider ID",
    cls=common.GradientOption,
    required=True,
)
@common.api_key_option
@common.options_file
def delete_storage_provider(id, api_key, options_file):
    command = commands.DeleteStorageProviderCommand(api_key=api_key)
    command.execute(id)
