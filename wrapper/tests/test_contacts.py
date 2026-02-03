import pytest
from unittest.mock import Mock, MagicMock
from ghl.endpoints.contacts import list_contacts, get_contact, create_contact, update_contact, delete_contact, search_contacts

@pytest.fixture
def mock_client():
    client = Mock()
    client.get = Mock()
    client.post = Mock()
    client.put = Mock()
    client.delete = Mock()
    return client

def test_list_contacts(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "contacts": [
            {"id": "1", "name": "John Doe", "email": "john@example.com", "phone": "123"},
            {"id": "2", "name": "Jane Doe", "email": "jane@example.com"}
        ],
        "meta": {"total": 2}
    }
    mock_client.get.return_value = mock_response

    result = list_contacts(mock_client, limit=10)

    mock_client.get.assert_called_with("/contacts/", params={"limit": 10})
    assert len(result["contacts"]) == 2
    assert result["contacts"][0]["id"] == "1"
    # essential fields check
    assert "phone" not in result["contacts"][0]

def test_list_contacts_verbose(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "contacts": [
            {"id": "1", "name": "John Doe", "email": "john@example.com", "phone": "123"},
        ],
        "meta": {"total": 1}
    }
    mock_client.get.return_value = mock_response

    result = list_contacts(mock_client, verbose=1)

    assert result["contacts"][0]["phone"] == "123"

def test_get_contact(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "contact": {"id": "1", "name": "John Doe", "email": "john@example.com"}
    }
    mock_client.get.return_value = mock_response

    result = get_contact(mock_client, "1")

    mock_client.get.assert_called_with("/contacts/1")
    assert result["id"] == "1"

def test_create_contact(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"contact": {"id": "1", "name": "John"}}
    mock_client.post.return_value = mock_response

    data = {"name": "John", "email": "john@example.com"}
    result = create_contact(mock_client, data)

    mock_client.post.assert_called_with("/contacts/", json=data)
    assert result["contact"]["id"] == "1"

def test_update_contact(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"contact": {"id": "1", "name": "John Updated"}}
    mock_client.put.return_value = mock_response

    data = {"name": "John Updated"}
    result = update_contact(mock_client, "1", data)

    mock_client.put.assert_called_with("/contacts/1", json=data)
    assert result["contact"]["name"] == "John Updated"

def test_delete_contact(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"success": True}
    mock_client.delete.return_value = mock_response

    result = delete_contact(mock_client, "1")

    mock_client.delete.assert_called_with("/contacts/1")
    assert result["success"] is True

def test_search_contacts(mock_client):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "contacts": [{"id": "1", "name": "John"}],
        "meta": {"total": 1}
    }
    mock_client.get.return_value = mock_response

    result = search_contacts(mock_client, query="John")

    mock_client.get.assert_called_with("/contacts/", params={"limit": 100, "query": "John"})
    assert len(result["contacts"]) == 1
