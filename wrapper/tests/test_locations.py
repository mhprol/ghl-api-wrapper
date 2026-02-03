import pytest
from unittest.mock import Mock, MagicMock
from ghl.endpoints.locations import list_locations, get_location, create_location, update_location, delete_location

@pytest.fixture
def mock_client():
    client = Mock()
    client.get = Mock()
    client.post = Mock()
    client.put = Mock()
    client.delete = Mock()
    return client

def test_list_locations(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "locations": [{"id": "1", "name": "Loc 1"}]
    }
    mock_client.get.return_value = mock_response

    result = list_locations(mock_client, limit=10, email="test@example.com")

    mock_client.get.assert_called_with("/locations/search", params={"limit": 10, "skip": 0, "email": "test@example.com"})
    assert len(result["locations"]) == 1

def test_get_location(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "location": {"id": "1", "name": "Loc 1"}
    }
    mock_client.get.return_value = mock_response

    result = get_location(mock_client, "1")

    mock_client.get.assert_called_with("/locations/1")
    assert result["location"]["id"] == "1"

def test_create_location(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"location": {"id": "1"}}
    mock_client.post.return_value = mock_response

    data = {"name": "Loc 1"}
    result = create_location(mock_client, data)

    mock_client.post.assert_called_with("/locations/", json=data)
    assert result["location"]["id"] == "1"

def test_update_location(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"location": {"id": "1", "name": "Loc 1 Updated"}}
    mock_client.put.return_value = mock_response

    data = {"name": "Loc 1 Updated"}
    result = update_location(mock_client, "1", data)

    mock_client.put.assert_called_with("/locations/1", json=data)
    assert result["location"]["name"] == "Loc 1 Updated"

def test_delete_location(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True}
    mock_client.delete.return_value = mock_response

    result = delete_location(mock_client, "1", delete_twilio_account=True)

    mock_client.delete.assert_called_with("/locations/1", params={"deleteTwilioAccount": True})
    assert result["success"] is True
