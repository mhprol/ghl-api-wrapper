import pytest
import httpx
from unittest.mock import Mock
from ghl.client import GHLClient

@pytest.fixture
def client_fixture():
    ghl_client = GHLClient(api_key="test_key")
    ghl_client.client = Mock(spec=httpx.Client)
    return ghl_client

def test_get_success(client_fixture):
    # Return a real response
    real_response = httpx.Response(200, json={"data": "ok"}, request=httpx.Request("GET", "https://example.com/test"))
    client_fixture.client.get.return_value = real_response

    response = client_fixture.get("/test")
    assert response.status_code == 200
    assert response.json() == {"data": "ok"}

def test_get_error_500(client_fixture):
    real_response = httpx.Response(500, content=b"Server Error", request=httpx.Request("GET", "https://example.com/test"))
    client_fixture.client.get.return_value = real_response

    # This should fail until we implement the fix
    with pytest.raises(httpx.HTTPStatusError):
        client_fixture.get("/test")

def test_error_message_enrichment(client_fixture):
    content = '{"message": "Validation failed", "code": 123}'
    real_response = httpx.Response(400, content=content, request=httpx.Request("POST", "https://example.com/test"))
    client_fixture.client.post.return_value = real_response

    # This should fail until we implement the fix
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        client_fixture.post("/test", json={})

    assert "Validation failed" in str(exc_info.value)
