import pytest
from unittest.mock import Mock, MagicMock
from ghl.endpoints.opportunities import list_opportunities, get_opportunity, create_opportunity, update_opportunity, delete_opportunity, list_pipelines

@pytest.fixture
def mock_client():
    client = Mock()
    client.location_id = "loc1"
    client.get = Mock()
    client.post = Mock()
    client.put = Mock()
    client.delete = Mock()
    return client

def test_list_opportunities(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "opportunities": [{"id": "1", "name": "Opp 1"}],
        "meta": {"total": 1}
    }
    mock_client.get.return_value = mock_response

    result = list_opportunities(mock_client, limit=10, query="test")

    mock_client.get.assert_called_with("/opportunities/search", params={"limit": 10, "q": "test", "location_id": "loc1"})
    assert len(result["opportunities"]) == 1

def test_get_opportunity(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "opportunity": {"id": "1", "name": "Opp 1"}
    }
    mock_client.get.return_value = mock_response

    result = get_opportunity(mock_client, "1")

    mock_client.get.assert_called_with("/opportunities/1")
    assert result["opportunity"]["id"] == "1"

def test_create_opportunity(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"opportunity": {"id": "1"}}
    mock_client.post.return_value = mock_response

    data = {"name": "Opp 1", "pipelineId": "pid1"}
    result = create_opportunity(mock_client, data)

    mock_client.post.assert_called_with("/opportunities/", json=data)
    assert result["opportunity"]["id"] == "1"

def test_update_opportunity(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"opportunity": {"id": "1", "name": "Opp 1 Updated"}}
    mock_client.put.return_value = mock_response

    data = {"name": "Opp 1 Updated"}
    result = update_opportunity(mock_client, "1", data)

    mock_client.put.assert_called_with("/opportunities/1", json=data)
    assert result["opportunity"]["name"] == "Opp 1 Updated"

def test_delete_opportunity(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True}
    mock_client.delete.return_value = mock_response

    result = delete_opportunity(mock_client, "1")

    mock_client.delete.assert_called_with("/opportunities/1")
    assert result["success"] is True

def test_list_pipelines(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "pipelines": [{"id": "pid1", "name": "Pipeline 1"}]
    }
    mock_client.get.return_value = mock_response

    result = list_pipelines(mock_client)

    mock_client.get.assert_called_with("/opportunities/pipelines", params={"locationId": "loc1"})
    assert result["pipelines"][0]["id"] == "pid1"
