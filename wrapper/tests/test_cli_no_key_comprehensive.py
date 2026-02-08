import pytest
from click.testing import CliRunner
from unittest.mock import patch
from ghl.cli import cli

@pytest.fixture
def runner():
    return CliRunner()

COMMANDS = [
    # Contacts
    ["contacts", "list"],
    ["contacts", "get", "1"],
    ["contacts", "create", "--data", "{}"],
    ["contacts", "update", "1", "--data", "{}"],
    ["contacts", "delete", "1"],
    ["contacts", "search", "--query", "q"],

    # Conversations
    ["conversations", "list"],
    ["conversations", "get", "1"],
    ["conversations", "create", "--data", "{}"],
    ["conversations", "update", "1", "--data", "{}"],
    ["conversations", "delete", "1"],
    ["conversations", "messages", "1"],

    # Opportunities
    ["opportunities", "list"],
    ["opportunities", "get", "1"],
    ["opportunities", "create", "--data", "{}"],
    ["opportunities", "update", "1", "--data", "{}"],
    ["opportunities", "delete", "1"],
    ["opportunities", "pipelines"],

    # Calendars
    ["calendars", "list"],
    ["calendars", "get", "1"],
    ["calendars", "create", "--data", "{}"],
    ["calendars", "update", "1", "--data", "{}"],
    ["calendars", "delete", "1"],
    ["calendars", "events", "--start-time", "1", "--end-time", "2"],

    # Workflows
    ["workflows", "list"],

    # Objects
    ["objects", "list-schemas"],
    ["objects", "get-schema", "key"],
    ["objects", "list", "key"],
    ["objects", "get", "key", "id"],
    ["objects", "create", "key", "--data", "{}"],
    ["objects", "update", "key", "id", "--data", "{}"],
    ["objects", "delete", "key", "id"],

    # Locations
    ["locations", "list"],
    ["locations", "get", "1"],
    ["locations", "create", "--data", "{}"],
    ["locations", "update", "1", "--data", "{}"],
    ["locations", "delete", "1"],
]

@pytest.mark.parametrize("args", COMMANDS)
def test_cli_no_key_commands(runner, args):
    # Ensure get_config returns empty
    with patch("ghl.cli.get_config", return_value={}):
        result = runner.invoke(cli, args)
        assert result.exit_code == 1
        assert "Error: API Key is missing" in result.output
