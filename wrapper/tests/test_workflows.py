import pytest
from unittest.mock import Mock, MagicMock
from ghl.endpoints.workflows import list_workflows

@pytest.fixture
def mock_client():
    client = Mock()
    client.location_id = "loc1"
    client.get = Mock()
    return client

def test_list_workflows(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "workflows": [{"id": "1", "name": "WF 1"}]
    }
    mock_client.get.return_value = mock_response

    result = list_workflows(mock_client)

    mock_client.get.assert_called_with("/workflows/", params={"locationId": "loc1"})
    assert len(result["workflows"]) == 1
