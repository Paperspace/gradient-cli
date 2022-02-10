from __future__ import annotations
from gql import gql, Client
from src.paperspace.http import http_request_adaptor

query = """
    mutation updateDeployment($input: UpdateDeploymentInput!) {
        updateDeployment(input: $input) {
            deployment {
                id
            }
        }
    }
"""

def update_deployment(id: str, name: str=None, project_id: str=None,
                      spec: dict=None, cluster_id: str=None) -> dict:
    client: Client = http_request_adaptor()
    input: dict = {
        'id': id,
    }
    if name is not None:
        input['name'] = name
    if project_id is not None:
        input['projectId'] = project_id
    if cluster_id is not None:
        input['clusterId'] = cluster_id
    if spec is not None:
        input['spec'] = spec

    params = {
        'input': input
    }

    return client.execute(
        gql(query),
        variable_values=params
    )['updateDeployment']['deployment']
