import pytest
import httpx
from unittest.mock import MagicMock, call

def test_init(ghl_client):
    assert ghl_client.api_key == "test_key"
    assert ghl_client.location_id is None

def test_init_oauth(ghl_client_oauth):
    assert ghl_client_oauth.client_id == "test_client_id"
    assert ghl_client_oauth.client_secret == "test_client_secret"
    assert ghl_client_oauth.refresh_token == "test_refresh_token"

def test_get_success(ghl_client, mock_httpx_client):
    response = MagicMock(spec=httpx.Response)
    response.status_code = 200
    response.json.return_value = {"data": "ok"}
    response.raise_for_status.return_value = None
    mock_httpx_client.get.return_value = response

    result = ghl_client.get("/test")

    assert result.status_code == 200
    assert result.json() == {"data": "ok"}
    mock_httpx_client.get.assert_called_once_with("/test", params=None)

def test_post_success(ghl_client, mock_httpx_client):
    response = MagicMock(spec=httpx.Response)
    response.status_code = 201
    response.json.return_value = {"id": "1"}
    response.raise_for_status.return_value = None
    mock_httpx_client.post.return_value = response

    result = ghl_client.post("/test", json={"foo": "bar"})

    assert result.status_code == 201
    mock_httpx_client.post.assert_called_once_with("/test", json={"foo": "bar"}, params=None)

def test_error_handling_enrichment(ghl_client, mock_httpx_client):
    response = MagicMock(spec=httpx.Response)
    response.status_code = 400
    response.json.return_value = {"message": "Invalid data"}
    response.raise_for_status.side_effect = httpx.HTTPStatusError("Bad Request", request=MagicMock(), response=response)
    response.content = b'{"message": "Invalid data"}'
    response.text = '{"message": "Invalid data"}'
    mock_httpx_client.get.return_value = response

    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        ghl_client.get("/test")

    assert "Invalid data" in str(exc_info.value)

def test_refresh_token_success(ghl_client_oauth, mock_httpx_client, mocker):
    # Mock the internal temporary client used in refresh_access_token
    mock_token_client = MagicMock(spec=httpx.Client)
    mock_token_response = MagicMock(spec=httpx.Response)
    mock_token_response.status_code = 200
    mock_token_response.json.return_value = {
        "access_token": "new_access_token",
        "refresh_token": "new_refresh_token"
    }
    mock_token_response.raise_for_status.return_value = None
    mock_token_client.post.return_value = mock_token_response
    mock_token_client.__enter__.return_value = mock_token_client
    mock_token_client.__exit__.return_value = None

    mocker.patch("httpx.Client", return_value=mock_token_client)

    # Setup the initial 401 response
    response_401 = MagicMock(spec=httpx.Response)
    response_401.status_code = 401
    response_401.raise_for_status.side_effect = httpx.HTTPStatusError("Unauthorized", request=MagicMock(), response=response_401)

    # Setup the retry 200 response
    response_200 = MagicMock(spec=httpx.Response)
    response_200.status_code = 200
    response_200.json.return_value = {"success": True}
    response_200.raise_for_status.return_value = None

    # Configure the mock client to return 401 first, then 200
    mock_httpx_client.get.side_effect = [response_401, response_200]

    # Execute
    result = ghl_client_oauth.get("/test")

    # Verify
    assert result.status_code == 200
    assert ghl_client_oauth.api_key == "new_access_token"
    assert ghl_client_oauth.refresh_token == "new_refresh_token"
    assert mock_httpx_client.headers["Authorization"] == "Bearer new_access_token"

    # Verify calls
    assert mock_httpx_client.get.call_count == 2
    mock_token_client.post.assert_called_once()

def test_refresh_token_failure(ghl_client_oauth, mock_httpx_client, mocker):
    # Mock token refresh failure
    mock_token_client = MagicMock(spec=httpx.Client)
    mock_token_response = MagicMock(spec=httpx.Response)
    mock_token_response.status_code = 400
    mock_token_response.raise_for_status.side_effect = httpx.HTTPStatusError("Bad Request", request=MagicMock(), response=mock_token_response)
    mock_token_client.post.return_value = mock_token_response
    mock_token_client.__enter__.return_value = mock_token_client
    mock_token_client.__exit__.return_value = None

    mocker.patch("httpx.Client", return_value=mock_token_client)

    response_401 = MagicMock(spec=httpx.Response)
    response_401.status_code = 401
    response_401.raise_for_status.side_effect = httpx.HTTPStatusError("Unauthorized", request=MagicMock(), response=response_401)

    mock_httpx_client.get.return_value = response_401

    with pytest.raises(httpx.HTTPStatusError):
        ghl_client_oauth.get("/test")

    assert mock_httpx_client.get.call_count == 1

def test_refresh_missing_credentials(ghl_client):
    # ghl_client has no client_id/secret
    with pytest.raises(ValueError, match="required for token refresh"):
        ghl_client.refresh_access_token()

def test_rate_limit_error(ghl_client, mock_httpx_client):
    response = MagicMock(spec=httpx.Response)
    response.status_code = 429
    response.raise_for_status.side_effect = httpx.HTTPStatusError("Too Many Requests", request=MagicMock(), response=response)
    mock_httpx_client.get.return_value = response

    with pytest.raises(httpx.HTTPStatusError):
        ghl_client.get("/test")
