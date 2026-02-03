import pytest
from unittest.mock import Mock, MagicMock
from ghl.endpoints.conversations import list_conversations, get_conversation, create_conversation, update_conversation, delete_conversation, get_messages

@pytest.fixture
def mock_client():
    client = Mock()
    client.location_id = "loc1"
    client.get = Mock()
    client.post = Mock()
    client.put = Mock()
    client.delete = Mock()
    return client

def test_list_conversations(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "conversations": [{"id": "1", "contactId": "c1"}],
        "total": 1
    }
    mock_client.get.return_value = mock_response

    result = list_conversations(mock_client, limit=10, status="all")

    mock_client.get.assert_called_with("/conversations/search", params={"limit": 10, "status": "all", "locationId": "loc1"})
    assert len(result["conversations"]) == 1

def test_get_conversation(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "conversation": {"id": "1", "contactId": "c1"}
    }
    mock_client.get.return_value = mock_response

    result = get_conversation(mock_client, "1")

    mock_client.get.assert_called_with("/conversations/1")
    assert result["conversation"]["id"] == "1"

def test_create_conversation(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True, "conversation": {"id": "1"}}
    mock_client.post.return_value = mock_response

    data = {"contactId": "c1", "locationId": "loc1"}
    result = create_conversation(mock_client, data)

    mock_client.post.assert_called_with("/conversations/", json=data)
    assert result["success"] is True

def test_update_conversation(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True}
    mock_client.put.return_value = mock_response

    data = {"unreadCount": 0}
    result = update_conversation(mock_client, "1", data)

    mock_client.put.assert_called_with("/conversations/1", json=data)
    assert result["success"] is True

def test_delete_conversation(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True}
    mock_client.delete.return_value = mock_response

    result = delete_conversation(mock_client, "1")

    mock_client.delete.assert_called_with("/conversations/1")
    assert result["success"] is True

def test_get_messages(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "messages": {"messages": [{"id": "m1", "body": "hello"}]}
    }
    mock_client.get.return_value = mock_response

    result = get_messages(mock_client, "1", limit=10)

    mock_client.get.assert_called_with("/conversations/1/messages", params={"limit": 10})
    assert result["messages"]["messages"][0]["id"] == "m1"
