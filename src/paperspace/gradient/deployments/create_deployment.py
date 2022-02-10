from __future__ import annotations
from gql import gql, Client
from src.paperspace.http import http_request_adaptor

query = """
    mutation createDeployment($input: CreateDeploymentInput!) {
        createDeployment(input: $input) {
            deployment {
                id
            }
        }
    }
"""

def create_deployment(name: str, project_id: str, spec: dict,
                      cluster_id: str=None) -> dict:
    client: Client = http_request_adaptor()
    params: dict = {
        'input': {
            'name': name,
            'clusterId': cluster_id,
            'projectId': project_id,
            'spec': spec
        }
    }

    return client.execute(
        gql(query),
        variable_values=params
    )['createDeployment']['deployment']
