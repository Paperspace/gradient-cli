from __future__ import annotations
from src.paperspace import session_decorator
from src.paperspace.session import Session
from gql import Client
from gql.transport.requests import RequestsHTTPTransport


@session_decorator
def http_request_adaptor(session: Session=None) -> Client:
    headers: dict[str, str] = {
        'Authorization': f'Bearer {session.api_key}',
    }

    transport: RequestsHTTPTransport = RequestsHTTPTransport(
        headers=headers,
        url=session.config['API_HOST'],
        verify=True,
        retries=3
    )

    return Client(transport=transport)
