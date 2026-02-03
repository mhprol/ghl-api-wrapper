import pytest
from unittest.mock import Mock, MagicMock
from ghl.endpoints.objects import list_schemas, get_schema, list_records, get_record, create_record, update_record, delete_record

@pytest.fixture
def mock_client():
    client = Mock()
    client.location_id = "loc1"
    client.get = Mock()
    client.post = Mock()
    client.put = Mock()
    client.delete = Mock()
    return client

def test_list_schemas(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "objects": [{"id": "1", "name": "Obj 1"}]
    }
    mock_client.get.return_value = mock_response

    result = list_schemas(mock_client)

    mock_client.get.assert_called_with("/objects/", params={"locationId": "loc1"})
    assert len(result["objects"]) == 1

def test_get_schema(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "object": {"id": "1", "key": "custom_objects.pet"}
    }
    mock_client.get.return_value = mock_response

    result = get_schema(mock_client, "custom_objects.pet")

    mock_client.get.assert_called_with("/objects/custom_objects.pet", params={"locationId": "loc1"})
    assert result["object"]["key"] == "custom_objects.pet"

def test_list_records(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "records": [{"id": "r1"}],
        "total": 1
    }
    mock_client.post.return_value = mock_response

    result = list_records(mock_client, "custom_objects.pet", limit=10, query="test")

    mock_client.post.assert_called_with("/objects/custom_objects.pet/records/search", json={"pageLimit": 10, "page": 1, "query": "test", "locationId": "loc1"})
    assert len(result["records"]) == 1

def test_get_record(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "record": {"id": "r1"}
    }
    mock_client.get.return_value = mock_response

    result = get_record(mock_client, "custom_objects.pet", "r1")

    mock_client.get.assert_called_with("/objects/custom_objects.pet/records/r1")
    assert result["record"]["id"] == "r1"

def test_create_record(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"record": {"id": "r1"}}
    mock_client.post.return_value = mock_response

    data = {"properties": {"name": "Buddy"}}
    result = create_record(mock_client, "custom_objects.pet", data)

    mock_client.post.assert_called_with("/objects/custom_objects.pet/records", json=data)
    assert result["record"]["id"] == "r1"

def test_update_record(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"record": {"id": "r1"}}
    mock_client.put.return_value = mock_response

    data = {"properties": {"name": "Buddy Updated"}}
    result = update_record(mock_client, "custom_objects.pet", "r1", data)

    mock_client.put.assert_called_with("/objects/custom_objects.pet/records/r1", json=data)
    assert result["record"]["id"] == "r1"

def test_delete_record(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True}
    mock_client.delete.return_value = mock_response

    result = delete_record(mock_client, "custom_objects.pet", "r1")

    mock_client.delete.assert_called_with("/objects/custom_objects.pet/records/r1")
    assert result["success"] is True
