from gql import Client
from gql.transport.requests import RequestsHTTPTransport


from .config import config

def graphql_client(api_key=None):
	if api_key is None:
		api_key = config.PAPERSPACE_API_KEY
	headers = {
		'Authorization': f'Bearer {api_key}',
	}
	transport = RequestsHTTPTransport(headers=headers, url=config.API_HOST, verify=True, retries=3)
	
	return Client(transport=transport)