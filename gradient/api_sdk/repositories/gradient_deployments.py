from gql import gql
from ..graphql import graphql_client


def create_deployment(name, project_id, spec, cluster_id=None):
	client = graphql_client()
	query = gql(
	"""
		mutation createDeployment($input: CreateDeploymentInput!) {
			createDeployment(input: $input) {
				deployment {
					id
				}
			}
		}
	"""
	)
	params = {
		"input": {
			"name": name,
			"clusterId": cluster_id,
			"projectId": project_id,
			"spec": spec,
		}
	}
	return client.execute(query, variable_values=params)['createDeployment']['deployment']


def update_deployment(id, name=None, project_id=None, spec=None, cluster_id=None):
	client = graphql_client()
	query = gql(
	"""
		mutation updateDeployment($input: UpdateDeploymentInput!) {
			updateDeployment(input: $input) {
				deployment {
					id
				}
			}
		}
	"""
	)

	input = {
		"id": id,
	}
	if name is not None:
		input["name"] = name
	if project_id is not None:
		input["projectId"] = project_id
	if cluster_id is not None:
		input["clusterId"] = cluster_id
	if spec is not None:
		input["spec"] = spec

	params = {
		"input": input	
	}
	return client.execute(query, variable_values=params)['updateDeployment']['deployment']


def get_deployment(id, first=100):
	client = graphql_client()
	query = gql(
	"""
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
							avatarUrl
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
	"""
	)
	params = {
		"id": id,
		"first": first,
	}
	return client.execute(query, variable_values=params)


def list_deployments(first=100):
	client = graphql_client()
	query = gql(
	"""
		query getDeployments($first: Int!) {
			deployments(first: $first) {
				nodes {
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
	)
	params = {
		"first": first,
	}
	return client.execute(query, variable_values=params)['deployments']['nodes']


def delete_deployment(id):
	client = graphql_client()
	query = gql(
	"""
		mutation deleteDeployment($input: DeleteDeploymentInput!) {
			deleteDeployment(input: $input) {
				deployment {
					id
				}
			}
		}
	"""
	)
	params = {
		"input": {
			"id": id,
		}
	}
	return client.execute(query, variable_values=params)['deleteDeployment']