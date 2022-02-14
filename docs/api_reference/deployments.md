# Gradient Deployments

Deployments are used to host models, serve inferences, and execute pre- and post-inference processing steps.

## `create_deployment()`

### Request

**Request Syntax**

```
from paperspace.gradient import deployments


deployment = deployments.create_deployment(
    name='string',
    project_id='string',
    spec={'key': 'value'},
    cluster_id='string'|None
)
```

**Parameters**

  - **name** (string) -- The human-readable name for a deployment. Must be unique within a Project among non-deleted deployments
  - **project_id** (string) -- The ID of the Project you want to associate this deployment to
  - **spec** (dictionary) -- the parsed [Deployment Spec](https://docs.paperspace.com/gradient/explore-train-deploy/deployments/deployment-spec)
  - **cluster_id** (string or None) -- Optional. The ID of the cluster you want to deploy onto

### Response

**Response Syntax**
```
{
    'id': 'd4e74a9c-b125-4bd7-b143-8f5c386df8a9'
}
```

**Response Structure**

  - (dict) -- The result of the operation and whether it was successful
    - **id** (string) -- ID of the deployment that was created


## `update_deployment()`

### Request

**Request Syntax**

```
from paperspace.gradient import deployments


deployment = deployments.update_deployment(
    name='string',
    project_id='string',
    spec={'key': 'value'},
    cluster_id='string'|None
)
```

**Parameters**

  - **name** (string) -- The human-readable name for the deployment. Must be unique within a Project among non-deleted deployments
  - **project_id** (string) -- The ID of the Project you want to associate this deployment to
  - **spec** (dictionary) -- the parsed [Deployment Spec](https://docs.paperspace.com/gradient/explore-train-deploy/deployments/deployment-spec)
  - **cluster_id** (string or None) -- Optional. The ID of the cluster you want to deploy onto

### Response

**Response Syntax**
```
{
    'id': 'd4e74a9c-b125-4bd7-b143-8f5c386df8a9'
}
```

**Response Structure**

  - (dict) -- The result of the operation and whether it was successful
    - **id** (string) -- ID of the deployment that was updated


## `delete_deployment()`

### Request

**Request Syntax**

```
from paperspace.gradient import deployments


deployment = deployments.delete_deployment(
    id='string'
)
```

**Parameters**

  - **id** (string) -- The ID of the deployment you wish to delete

### Response

**Response Syntax**
```
{
    'id': 'd4e74a9c-b125-4bd7-b143-8f5c386df8a9'
}
```

**Response Structure**

  - (dict) -- The result of the operation and whether it was successful
    - **id** (string) -- ID of the deployment that was deleted


## `list_deployments()`

### Request

**Request Syntax**

```
from paperspace.gradient import deployments


deployment = deployments.list_deployments(
    name='string'|None,
    project_id='string'|None,
    cluster_id='string'|None,
    first=100|None
)
```

**Parameters**

  - **name** (string or None) -- Optional The human-readable deployment name you would like to filter on
  - **project_id** (string or None) --Optional.  The ID of the Project you wish to restrict your search to
  - **cluster_id** (string or None) -- Optional. The ID of the cluster you want to restrict your search to

### Response

**Response Syntax**
```
[{
  'id': 'd4e74a9c-b125-4bd7-b143-8f5c386df8a9',
  'name': 'Test Deployment',
  'deploymentSpecs': {
    'nodes': [{
      'id': '8f5c4a9c-4bd7-b143-b125-8f5c386df8a9',
      'data': {
        'image': 'tensorflow/serving',
        'port': 8501,
        'resources': {
          'instanceType': 'A100',
          'replicas': 1
        }
      },
      'endpointUrl': 'https://model-endpoint.example.com',
      'actor': {
        'fullName': 'John Smith'
      }
    }]
  }
}]
```

**Response Structure**

  - (dict) -- The result of the operation and whether it was successful
    - **id** (string) -- ID of the deployment
    - **name** (string) -- The name of the deployment
    - **deploymentSpecs** (dict) -- The specification for the deployment
      - **nodes** (list) -- Nodes in the response
        - (dict) -- One or more individual deployment specs, ordered descending by date of creation
          - **id** (string) -- The ID of the deployment spec
          - **data** (dict) -- The spec data
            - **image** (string) -- The container image being used
            - **port** (int) -- The container port being exposed to the host
            - **resources** (dict) -- The physical hardware being deployed onto
              - **instanceType** (string) -- The Paperspace instance being used
              - **replicas** (int) -- The number of replicas of the deployment
          - **endpointUrl** (string) -- The endpoint the deployment is accessible by
          - **actor** (dict) -- Information about the user who created this deployment spec
            - **fullName** (string) -- First and last name


## `get_deployment()`

### Request

**Request Syntax**

```
from paperspace.gradient import deployments


deployment = deployments.get_deployment(
    id='string'
)
```

**Parameters**

  - **id** (string) -- The ID of the deployment to query

### Response

**Response Syntax**
```
{
  'id': 'd4e74a9c-b125-4bd7-b143-8f5c386df8a9',
  'name': 'Test Deployment',
  'deploymentSpecs': {
    'nodes': [{
      'id': '8f5c4a9c-4bd7-b143-b125-8f5c386df8a9',
      'data': {
        'image': 'tensorflow/serving',
        'port': 8501,
        'resources': {
          'instanceType': 'A100',
          'replicas': 1
        }
      },
      'endpointUrl': 'https://model-endpoint.example.com',
      'actor': {
        'fullName': 'John Smith'
      }
    }]
  }
}
```

**Response Structure**

  - (dict) -- The result of the operation and whether it was successful
    - **id** (string) -- ID of the deployment
    - **name** (string) -- The name of the deployment
    - **deploymentSpecs** (dict) -- The specification for the deployment
      - **nodes** (list) -- Nodes in the response
        - (dict) -- One or more individual deployment specs, ordered descending by date of creation
          - **id** (string) -- The ID of the deployment spec
          - **data** (dict) -- The spec data
            - **image** (string) -- The container image being used
            - **port** (int) -- The container port being exposed to the host
            - **resources** (dict) -- The physical hardware being deployed onto
              - **instanceType** (string) -- The Paperspace instance being used
              - **replicas** (int) -- The number of replicas of the deployment
          - **endpointUrl** (string) -- The endpoint the deployment is accessible by
          - **actor** (dict) -- Information about the user who created this deployment spec
            - **fullName** (string) -- First and last name
