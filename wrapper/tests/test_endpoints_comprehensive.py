import pytest
from unittest.mock import Mock, MagicMock
from ghl.endpoints import calendars, conversations, locations, objects, opportunities, workflows

@pytest.fixture
def mock_client():
    client = Mock()
    client.location_id = "loc_123"
    client.get = Mock()
    client.post = Mock()
    client.put = Mock()
    client.delete = Mock()
    # Mock return values with defaults to avoid KeyErrors or empty responses failing logic if any
    client.get.return_value.json.return_value = {}
    client.post.return_value.json.return_value = {}
    client.put.return_value.json.return_value = {}
    client.delete.return_value.json.return_value = {}
    return client

# Calendars
def test_list_calendars(mock_client):
    calendars.list_calendars(mock_client)
    mock_client.get.assert_called_with("/calendars/", params={"locationId": "loc_123"})

def test_list_events(mock_client):
    calendars.list_events(mock_client, "1000", "2000")
    mock_client.get.assert_called_with("/calendars/events", params={"startTime": "1000", "endTime": "2000", "locationId": "loc_123"})

# Conversations
def test_list_conversations(mock_client):
    conversations.list_conversations(mock_client)
    mock_client.get.assert_called_with("/conversations/search", params={"limit": 20, "locationId": "loc_123"})

def test_get_conversation(mock_client):
    conversations.get_conversation(mock_client, "conv_1")
    mock_client.get.assert_called_with("/conversations/conv_1")

# Locations
def test_list_locations(mock_client):
    locations.list_locations(mock_client)
    mock_client.get.assert_called_with("/locations/search", params={"limit": 10, "skip": 0})

def test_get_location(mock_client):
    locations.get_location(mock_client, "loc_1")
    mock_client.get.assert_called_with("/locations/loc_1")

# Opportunities
def test_list_opportunities(mock_client):
    opportunities.list_opportunities(mock_client)
    # Note: opportunities.py uses "location_id" (snake_case) while others use "locationId" (camelCase) usually.
    # Checking opportunities.py content: params["location_id"] = client.location_id
    mock_client.get.assert_called_with("/opportunities/search", params={"limit": 20, "location_id": "loc_123"})

def test_list_pipelines(mock_client):
    opportunities.list_pipelines(mock_client)
    mock_client.get.assert_called_with("/opportunities/pipelines", params={"locationId": "loc_123"})

# Workflows
def test_list_workflows(mock_client):
    workflows.list_workflows(mock_client)
    mock_client.get.assert_called_with("/workflows/", params={"locationId": "loc_123"})

# Objects
def test_list_schemas(mock_client):
    objects.list_schemas(mock_client)
    mock_client.get.assert_called_with("/objects/", params={"locationId": "loc_123"})

def test_list_records(mock_client):
    # list_records uses POST to /objects/{schema_key}/records/search
    # It builds data dict.
    # list_records(client, schema_key, limit=20, query=None, location_id=None)
    # data = {"pageLimit": 20, "page": 1, "locationId": "loc_123"}
    objects.list_records(mock_client, "key")
    # Check that post was called with correct path and json data contains locationId
    # objects.py line: response = client.post(f"/objects/{schema_key}/records/search", json=data)
    mock_client.post.assert_called_with("/objects/key/records/search", json={"pageLimit": 20, "page": 1, "locationId": "loc_123"})

def test_get_calendar(mock_client):
    calendars.get_calendar(mock_client, "1")
    mock_client.get.assert_called_with("/calendars/1")

def test_create_calendar(mock_client):
    calendars.create_calendar(mock_client, {})
    mock_client.post.assert_called_with("/calendars/", json={})

def test_update_calendar(mock_client):
    calendars.update_calendar(mock_client, "1", {})
    mock_client.put.assert_called_with("/calendars/1", json={})

def test_delete_calendar(mock_client):
    calendars.delete_calendar(mock_client, "1")
    mock_client.delete.assert_called_with("/calendars/1")

def test_get_event(mock_client):
    calendars.get_event(mock_client, "1")
    mock_client.get.assert_called_with("/calendars/events/appointments/1")

def test_create_event(mock_client):
    calendars.create_event(mock_client, {})
    mock_client.post.assert_called_with("/calendars/events/appointments", json={})

def test_update_event(mock_client):
    calendars.update_event(mock_client, "1", {})
    mock_client.put.assert_called_with("/calendars/events/appointments/1", json={})

def test_delete_event(mock_client):
    calendars.delete_event(mock_client, "1")
    mock_client.delete.assert_called_with("/calendars/events/1")
