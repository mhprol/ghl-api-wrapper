import json
import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock, patch
from ghl.cli import cli

@pytest.fixture
def runner():
    return CliRunner()

def test_cli_help(runner):
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "GoHighLevel CLI Wrapper" in result.output

def test_cli_no_key(runner):
    # Ensure get_config returns empty if no key provided and no config file
    with patch("ghl.cli.get_config", return_value={}):
        result = runner.invoke(cli, ["contacts", "list"])
        assert result.exit_code == 1
        assert "Error: API Key is missing" in result.output

@patch("ghl.cli.GHLClient")
@patch("ghl.endpoints.contacts.list_contacts")
def test_contacts_list(mock_list_contacts, mock_client_cls, runner):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client
    mock_list_contacts.return_value = {"contacts": []}

    result = runner.invoke(cli, ["--api-key", "test_key", "contacts", "list"])

    assert result.exit_code == 0
    assert json.loads(result.output) == {"contacts": []}
    mock_client_cls.assert_called_with("test_key", None)
    mock_list_contacts.assert_called_with(mock_client, 20, None, None, 0)

@patch("ghl.cli.GHLClient")
@patch("ghl.endpoints.contacts.create_contact")
def test_contacts_create_with_data(mock_create_contact, mock_client_cls, runner):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client
    mock_create_contact.return_value = {"id": "123"}

    data = '{"name": "John"}'
    result = runner.invoke(cli, ["--api-key", "test_key", "contacts", "create", "--data", data])

    assert result.exit_code == 0
    assert json.loads(result.output) == {"id": "123"}
    mock_create_contact.assert_called_with(mock_client, {"name": "John"})

@patch("ghl.cli.GHLClient")
@patch("ghl.endpoints.contacts.create_contact")
def test_contacts_create_with_file(mock_create_contact, mock_client_cls, runner, tmp_path):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client
    mock_create_contact.return_value = {"id": "123"}

    data_file = tmp_path / "data.json"
    data_file.write_text('{"name": "John"}')

    result = runner.invoke(cli, ["--api-key", "test_key", "contacts", "create", "--file", str(data_file)])

    assert result.exit_code == 0
    assert json.loads(result.output) == {"id": "123"}
    mock_create_contact.assert_called_with(mock_client, {"name": "John"})

@patch("ghl.cli.get_config")
@patch("ghl.cli.GHLClient")
def test_cli_config_loading(mock_client_cls, mock_get_config, runner):
    mock_get_config.return_value = {"api_key": "config_key", "location_id": "config_loc"}

    # Mocking a command that does nothing but pass
    with patch("ghl.endpoints.contacts.list_contacts") as mock_list:
        mock_list.return_value = {}
        result = runner.invoke(cli, ["contacts", "list"])

    assert result.exit_code == 0
    # get_config called with None, None because no args passed
    mock_get_config.assert_called()
    mock_client_cls.assert_called_with("config_key", "config_loc")

@patch("ghl.cli.GHLClient")
@patch("ghl.endpoints.contacts.list_contacts")
def test_contacts_list_exception(mock_list_contacts, mock_client_cls, runner):
    mock_client = MagicMock()
    mock_client_cls.return_value = mock_client
    mock_list_contacts.side_effect = Exception("API Error")

    result = runner.invoke(cli, ["--api-key", "test_key", "contacts", "list"])

    assert result.exit_code == 1
    assert "API Error" in result.output
