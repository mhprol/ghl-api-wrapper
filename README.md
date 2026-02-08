# GoHighLevel API CLI Wrapper

A comprehensive Python client library and CLI tool for the GoHighLevel (GHL) API v2.

For AI agents using this library, please refer to the [AI Manual](docs/AI-MANUAL.md) for optimized patterns and structured references.

## Installation

This package requires Python 3.11+.

```bash
cd wrapper
pip install -e .
```

Dependencies:
- `click` (for CLI)
- `httpx` (for HTTP requests)
- `pydantic` (for data validation)

## Quick Start

### 1. Configuration

You need a GHL API Key and Location ID. You can set them via environment variables:

```bash
export GHL_API_KEY="your_api_key"
export GHL_LOCATION_ID="your_location_id"
```

Or create a config file at `~/.config/ghl/config.json`:

```json
{
  "api_key": "your_api_key",
  "location_id": "your_location_id"
}
```

### 2. Python Client Usage

```python
from ghl.client import GHLClient
from ghl.endpoints import contacts

# Initialize client (uses env vars if not provided)
client = GHLClient(api_key="your_api_key", location_id="your_location_id")

# List contacts
response = contacts.list_contacts(client, limit=5)
print(response['contacts'])
```

## CLI Reference

The `ghl` command allows you to interact with the API from your terminal.

### Basic Usage

```bash
ghl [OPTIONS] COMMAND [ARGS]...
```

**Global Options:**
- `--api-key TEXT`: Override API Key.
- `--location-id TEXT`: Override Location ID.
- `-v, --verbose`: Increase verbosity (show more fields).
- `--help`: Show help message.

### Common Commands

**Contacts**
```bash
# List contacts
ghl contacts list --limit 10

# Get a contact
ghl contacts get <contact_id>

# Create a contact
ghl contacts create --data '{"email": "test@example.com", "firstName": "Test"}'

# Search contacts
ghl contacts search --query "john"
```

**Conversations**
```bash
# List conversations
ghl conversations list --status unread

# Get messages
ghl conversations messages <conversation_id>
```

**Opportunities**
```bash
# List opportunities
ghl opportunities list --status open

# List pipelines
ghl opportunities pipelines
```

**Calendars**
```bash
# List calendars
ghl calendars list

# List events
ghl calendars events --start-time 1698300000000 --end-time 1698400000000
```

**Workflows**
```bash
# List workflows
ghl workflows list
```

**Custom Objects**
```bash
# List schemas
ghl objects list-schemas

# List records for a schema
ghl objects list <schema_key>
```

**Locations (Sub-accounts)**
```bash
# List locations
ghl locations list
```

## API Client Usage Guide

The library is structured with a central `GHLClient` and functional endpoint modules.

### The Client

```python
from ghl.client import GHLClient

client = GHLClient(api_key="...", location_id="...")
```

### Endpoint Modules

Import specific modules from `ghl.endpoints`:

- `contacts`
- `conversations`
- `opportunities`
- `calendars`
- `workflows`
- `objects`
- `locations`

Example:

```python
from ghl.endpoints import opportunities

# List pipelines to find stage IDs
pipelines = opportunities.list_pipelines(client)

# Create an opportunity
opportunities.create_opportunity(client, {
    "pipelineId": "...",
    "stageId": "...",
    "title": "New Deal",
    "status": "open"
})
```

## Configuration Reference

The CLI and Client resolve configuration in the following order:

1.  **CLI Arguments** (`--api-key`, `--location-id`)
2.  **Environment Variables** (`GHL_API_KEY`, `GHL_LOCATION_ID`)
3.  **Config File** (`~/.config/ghl/config.json`)

## Authentication & Token Refresh

The client supports automatic OAuth token refresh if initialized with `client_id`, `client_secret`, and `refresh_token`.

```python
client = GHLClient(
    api_key="current_access_token",
    location_id="location_id",
    client_id="your_client_id",
    client_secret="your_client_secret",
    refresh_token="your_refresh_token"
)
```

If the API returns a `401 Unauthorized` error, the client will automatically:
1.  Request a new access token using the refresh token.
2.  Update the client's internal state with the new token.
3.  Retry the original request.

## Error Handling

The client uses `httpx` and raises `httpx.HTTPStatusError` for 4xx/5xx responses. The error message is enriched with details from the API response to make debugging easier.

```python
import httpx
from ghl.endpoints import contacts

try:
    contacts.get_contact(client, "invalid_id")
except httpx.HTTPStatusError as e:
    print(f"Error: {e}")
    # e.response.json() contains API error details
```

## Rate Limits and Pagination

### Rate Limits
The GHL API enforces rate limits (e.g., 100 requests per 10 seconds per location). The client handles `401 Unauthorized` automatically, but `429 Too Many Requests` must be handled by your application logic.

```python
import time
import httpx

try:
    response = client.get("/contacts/")
except httpx.HTTPStatusError as e:
    if e.response.status_code == 429:
        print("Rate limit exceeded. Waiting...")
        time.sleep(5)
        # Implement retry logic here
```

### Pagination
List endpoints typically return a `meta` dictionary containing pagination information. You can use this to iterate through pages.

```python
# Example of manual pagination handling
contacts_list = []
params = {"limit": 20}
while True:
    response = client.get("/contacts/", params=params)
    data = response.json()
    contacts_list.extend(data.get("contacts", []))

    meta = data.get("meta", {})
    # Check if there is a next page indicator (this varies by endpoint, check meta structure)
    if "nextPageUrl" in meta and meta["nextPageUrl"]:
        # Extract next page params or update params for next call
        # specific logic depends on the endpoint's pagination strategy (e.g. startAfterId)
        break # simplified for example
    else:
        break
```

## Common Workflows

### Fetch Contact and Add Note

```python
from ghl.endpoints import contacts

# 1. Get contact
contact = contacts.get_contact(client, "contact_id")

# 2. Add a note to the contact
note_data = {
    "body": "Followed up with client regarding proposal.",
    "userId": "user_id"
}
# Assuming endpoint implementation supports notes (check specific endpoint file)
# notes.create_note(client, contact['id'], note_data)
```

## Contributing

Contributions are welcome! Please follow these steps:
1.  Fork the repository.
2.  Create a feature branch.
3.  Install dependencies: `cd wrapper && pip install -e .`
4.  Run tests: `pytest`
5.  Commit your changes.
6.  Push to the branch.
7.  Open a Pull Request.

## License

This project is licensed under the CC0 1.0 Universal.
