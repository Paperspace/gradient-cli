import datetime

import attr


@attr.s
class Deployment(object):
    """
    Deployment class

    Deploy any model as a high-performance, low-latency micro-service with a RESTful API. Easily monitor, scale, and
    version deployments. Deployments take a trained model and expose them as a persistent service at a known, secure
    URL endpoint.

    :param str id_: deployment id
    :param str name: Human-friendly name for new model deployment
    :param str endpoint: url address to deployment, for example::

        ``https://services.paperspace.io/model-serving/<your-model-id>:predict``
    :param str api_type: api type of deployment
        Options::

        "GPRC"
        "REST"
    :param str state: state of Deployment
        Options::

        "BUILDING"
        "PROVISIONING"
        "STARTING"
        "RUNNING"
        "STOPPING"
        "STOPPED"
        "ERROR"
    :param str model_id: model id
    :param str project_id: project id
    :param str image_url: Docker image for model deployment
    :param str deployment_type: Model deployment type.
    :param str machine_type: Type of machine for new deployment
        Options::

        "G1"
        "G6"
        "G12"
        "K80"
        "P100"
        "GV100"
    :param int instance_count: Number of machine instances

    """
    id = attr.ib(type=str, default=None)
    name = attr.ib(type=str, default=None)
    endpoint = attr.ib(type=str, default=None)
    api_type = attr.ib(type=str, default=None)

    state = attr.ib(type=str, default=None)

    model_id = attr.ib(type=str, default=None)
    project_id = attr.ib(type=str, default=None)

    image_url = attr.ib(type=str, default=None)
    deployment_type = attr.ib(type=str, default=None)
    machine_type = attr.ib(type=str, default=None)
    instance_count = attr.ib(type=int, default=None)
    container_model_path = attr.ib(type=str, default=None)
    image_username = attr.ib(type=str, default=None)
    image_password = attr.ib(type=str, default=None)
    image_server = attr.ib(type=str, default=None)
    container_url_path = attr.ib(type=str, default=None)
    endpoint_url_path = attr.ib(type=str, default=None)
    method = attr.ib(type=str, default=None)
    docker_args = attr.ib(type=list, default=None)
    env = attr.ib(type=dict, default=None)
    ports = attr.ib(type=str, default=None)
    auth_username = attr.ib(type=str, default=None)
    auth_password = attr.ib(type=str, default=None)
    cluster_id = attr.ib(type=int, default=None)
    tags = attr.ib(type=list, factory=list)
    command = attr.ib(type=str, default=None)
    workspace_url = attr.ib(type=str, default=None)
    workspace_ref = attr.ib(type=str, default=None)
    workspace_username = attr.ib(type=str, default=None)
    workspace_password = attr.ib(type=str, default=None)
    metrics_url = attr.ib(type=str, default=None)

    dt_created = attr.ib(type=datetime.datetime, default=None)
    dt_modified = attr.ib(type=datetime.datetime, default=None)
    dt_started = attr.ib(type=datetime.datetime, default=None)
    dt_stopped = attr.ib(type=datetime.datetime, default=None)
    dt_deleted = attr.ib(type=datetime.datetime, default=None)
