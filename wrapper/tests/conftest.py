import pytest
import httpx
from unittest.mock import MagicMock
from ghl.client import GHLClient

@pytest.fixture
def mock_httpx_client():
    client = MagicMock(spec=httpx.Client)
    client.headers = {"Authorization": "Bearer test_key"}
    return client

@pytest.fixture
def ghl_client(mock_httpx_client):
    client = GHLClient(api_key="test_key", client=mock_httpx_client)
    return client

@pytest.fixture
def ghl_client_oauth(mock_httpx_client):
    client = GHLClient(
        api_key="test_key",
        client=mock_httpx_client,
        client_id="test_client_id",
        client_secret="test_client_secret",
        refresh_token="test_refresh_token"
    )
    return client
