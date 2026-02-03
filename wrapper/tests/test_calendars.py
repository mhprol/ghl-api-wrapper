import pytest
from unittest.mock import Mock, MagicMock
from ghl.endpoints.calendars import list_calendars, get_calendar, create_calendar, update_calendar, delete_calendar, list_events

@pytest.fixture
def mock_client():
    client = Mock()
    client.location_id = "loc1"
    client.get = Mock()
    client.post = Mock()
    client.put = Mock()
    client.delete = Mock()
    return client

def test_list_calendars(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "calendars": [{"id": "1", "name": "Cal 1"}]
    }
    mock_client.get.return_value = mock_response

    result = list_calendars(mock_client)

    mock_client.get.assert_called_with("/calendars/", params={"locationId": "loc1"})
    assert len(result["calendars"]) == 1

def test_get_calendar(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "calendar": {"id": "1", "name": "Cal 1"}
    }
    mock_client.get.return_value = mock_response

    result = get_calendar(mock_client, "1")

    mock_client.get.assert_called_with("/calendars/1")
    assert result["calendar"]["id"] == "1"

def test_create_calendar(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"calendar": {"id": "1"}}
    mock_client.post.return_value = mock_response

    data = {"name": "Cal 1"}
    result = create_calendar(mock_client, data)

    mock_client.post.assert_called_with("/calendars/", json=data)
    assert result["calendar"]["id"] == "1"

def test_update_calendar(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"calendar": {"id": "1", "name": "Cal 1 Updated"}}
    mock_client.put.return_value = mock_response

    data = {"name": "Cal 1 Updated"}
    result = update_calendar(mock_client, "1", data)

    mock_client.put.assert_called_with("/calendars/1", json=data)
    assert result["calendar"]["name"] == "Cal 1 Updated"

def test_delete_calendar(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True}
    mock_client.delete.return_value = mock_response

    result = delete_calendar(mock_client, "1")

    mock_client.delete.assert_called_with("/calendars/1")
    assert result["success"] is True

def test_list_events(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "events": [{"id": "e1", "title": "Event 1"}]
    }
    mock_client.get.return_value = mock_response

    result = list_events(mock_client, start_time="1000", end_time="2000")

    mock_client.get.assert_called_with("/calendars/events", params={"startTime": "1000", "endTime": "2000", "locationId": "loc1"})
    assert len(result["events"]) == 1
