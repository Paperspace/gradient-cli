from __future__ import annotations
from gql import gql, Client
from src.paperspace.http import http_request_adaptor

query = """
    query getDeployments(
        $first: Int!
        $projectId: String
        $clusterId: String
        $name: String
    ) {
        deployments(
            first: $first
            projectId: $projectId
            name: $name
        ) {
            nodes {
                id
                name
                deploymentSpecs(first: $first, clusterId: $clusterId) {
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
                            avatarUrl
                            fullName
                        }
                        deploymentRuns(first: $first) {
                            nodes {
                                id
                                availableReplicas
                                readyReplicas
                                replicas
                                deploymentRunInstances(first: $first) {
                                    nodes {
                                        id
                                        phase
                                        dtStarted
                                        dtFinished
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
"""

def list_deployments(name: str=None, project_id: str=None,
                     cluster_id: str=None, first: int=100) -> dict:
    client: Client = http_request_adaptor()
    params: dict = {
        'name': name,
        'clusterId': cluster_id,
        'projectId': project_id,
        'first': first
    }

    return client.execute(
        gql(query),
        variable_values=params
    )['deployments']['nodes']
