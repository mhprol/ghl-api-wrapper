import json
import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock, patch
from ghl.cli import cli

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def mock_client_cls():
    with patch("ghl.cli.GHLClient") as mock:
        yield mock

@pytest.fixture
def mock_get_config():
    with patch("ghl.cli.get_config") as mock:
        mock.return_value = {"api_key": "test_key", "location_id": "test_loc"}
        yield mock

COMMANDS = [
    # Contacts (already partially covered but good to ensure)
    (["contacts", "list"], "ghl.endpoints.contacts.list_contacts"),
    (["contacts", "get", "1"], "ghl.endpoints.contacts.get_contact"),
    (["contacts", "delete", "1"], "ghl.endpoints.contacts.delete_contact"),

    # Conversations
    (["conversations", "list"], "ghl.endpoints.conversations.list_conversations"),
    (["conversations", "get", "1"], "ghl.endpoints.conversations.get_conversation"),
    (["conversations", "delete", "1"], "ghl.endpoints.conversations.delete_conversation"),
    (["conversations", "messages", "1"], "ghl.endpoints.conversations.get_messages"),

    # Opportunities
    (["opportunities", "list"], "ghl.endpoints.opportunities.list_opportunities"),
    (["opportunities", "get", "1"], "ghl.endpoints.opportunities.get_opportunity"),
    (["opportunities", "delete", "1"], "ghl.endpoints.opportunities.delete_opportunity"),
    (["opportunities", "pipelines"], "ghl.endpoints.opportunities.list_pipelines"),

    # Calendars
    (["calendars", "list"], "ghl.endpoints.calendars.list_calendars"),
    (["calendars", "get", "1"], "ghl.endpoints.calendars.get_calendar"),
    (["calendars", "delete", "1"], "ghl.endpoints.calendars.delete_calendar"),
    (["calendars", "events", "--start-time", "1", "--end-time", "2"], "ghl.endpoints.calendars.list_events"),

    # Workflows
    (["workflows", "list"], "ghl.endpoints.workflows.list_workflows"),

    # Objects
    (["objects", "list-schemas"], "ghl.endpoints.objects.list_schemas"),
    (["objects", "get-schema", "key"], "ghl.endpoints.objects.get_schema"),
    (["objects", "list", "key"], "ghl.endpoints.objects.list_records"),
    (["objects", "get", "key", "id"], "ghl.endpoints.objects.get_record"),
    (["objects", "delete", "key", "id"], "ghl.endpoints.objects.delete_record"),

    # Locations
    (["locations", "list"], "ghl.endpoints.locations.list_locations"),
    (["locations", "get", "1"], "ghl.endpoints.locations.get_location"),
    (["locations", "delete", "1"], "ghl.endpoints.locations.delete_location"),
]

@pytest.mark.parametrize("args, mock_target", COMMANDS)
def test_cli_commands(runner, mock_client_cls, mock_get_config, args, mock_target):
    with patch(mock_target) as mock_func:
        mock_func.return_value = {}
        result = runner.invoke(cli, args)
        if result.exit_code != 0:
             print(result.output)
        assert result.exit_code == 0
        mock_func.assert_called()

# Test create/update commands which require --data
CREATE_UPDATE_COMMANDS = [
    (["contacts", "update", "1", "--data", "{}"], "ghl.endpoints.contacts.update_contact"),
    (["conversations", "create", "--data", "{}"], "ghl.endpoints.conversations.create_conversation"),
    (["conversations", "update", "1", "--data", "{}"], "ghl.endpoints.conversations.update_conversation"),
    (["opportunities", "create", "--data", "{}"], "ghl.endpoints.opportunities.create_opportunity"),
    (["opportunities", "update", "1", "--data", "{}"], "ghl.endpoints.opportunities.update_opportunity"),
    (["calendars", "create", "--data", "{}"], "ghl.endpoints.calendars.create_calendar"),
    (["calendars", "update", "1", "--data", "{}"], "ghl.endpoints.calendars.update_calendar"),
    (["objects", "create", "key", "--data", "{}"], "ghl.endpoints.objects.create_record"),
    (["objects", "update", "key", "id", "--data", "{}"], "ghl.endpoints.objects.update_record"),
    (["locations", "create", "--data", "{}"], "ghl.endpoints.locations.create_location"),
    (["locations", "update", "1", "--data", "{}"], "ghl.endpoints.locations.update_location"),
]

@pytest.mark.parametrize("args, mock_target", CREATE_UPDATE_COMMANDS)
def test_cli_create_update_commands(runner, mock_client_cls, mock_get_config, args, mock_target):
    with patch(mock_target) as mock_func:
        mock_func.return_value = {}
        result = runner.invoke(cli, args)
        if result.exit_code != 0:
             print(result.output)
        assert result.exit_code == 0
        mock_func.assert_called()
