from __future__ import annotations
from gql import gql, Client
from src.paperspace.http import http_request_adaptor

query = """
    mutation deleteDeployment($input: DeleteDeploymentInput!) {
        deleteDeployment(input: $input) {
            deployment {
                id
            }
        }
    }
"""

def delete_deployment(id: str) -> dict:
    client: Client = http_request_adaptor()
    params = {
        'input': {
            'id': id,
        }
    }

    return client.execute(
        gql(query),
        variable_values=params
    )['deleteDeployment']
