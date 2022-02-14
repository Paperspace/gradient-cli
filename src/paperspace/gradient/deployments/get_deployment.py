from __future__ import annotations
from gql import gql, Client
from src.paperspace.http import http_request_adaptor

query = """
    query getDeployment($id: UUID!, $first: Int!) {
        deployment(id: $id) {
            id
            name
            deploymentSpecs(first: $first) {
                nodes {
                    id
                    data {
                        image
                        port
                        resources {
                            instanceType
                            replicas
                        }
                    }
                    endpointUrl
                    actor {
                        fullName
                    }
                    cluster {
                        id
                    }
                    data {
                        command
                        env {
                            name
                            value
                        }
                        image
                        models {
                            id
                            path
                        }
                        port
                        resources {
                            replicas
                        }
                    }
                }
            }
        }
    }
"""

def get_deployment(id: str, first: int=100) -> dict:
    client: Client = http_request_adaptor()
    params: dict = {
        'id': id,
        'first': first
    }

    return client.execute(
        gql(query),
        variable_values=params
    )
