# GoHighLevel (GHL) API Python Wrapper & CLI

A comprehensive Python client library and CLI tool for the GoHighLevel (GHL) API v2.

## 🚀 Project Overview

This project provides a robust Python wrapper for interacting with the GoHighLevel API. It includes:
- A **Python Client Library** (`ghl`) for integrating GHL into your applications.
- A **CLI Tool** (`ghl`) for managing resources directly from the terminal.
- Support for key GHL resources: Contacts, Conversations, Opportunities, Calendars, Workflows, Custom Objects, and Locations.

## 📦 Installation

This package requires Python 3.11+.

### From Source

```bash
git clone https://github.com/GoHighLevel/api-v2-docs.git
cd api-v2-docs/wrapper
pip install -e .
```

### Dependencies

- `click` (for CLI)
- `httpx` (for HTTP requests)
- `pydantic` (for data validation)

## ⚡ Quick Start

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

# Create a contact
new_contact = contacts.create_contact(client, data={
    "email": "test@example.com",
    "firstName": "John",
    "lastName": "Doe"
})
print(new_contact)
```

## 💻 CLI Guide

The `ghl` command allows you to interact with the API from your terminal.

### Basic Usage

```bash
ghl [OPTIONS] COMMAND [ARGS]...
```

**Global Options:**
- `--api-key TEXT`: Override API Key.
- `--location-id TEXT`: Override Location ID.
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

## 📚 API Client Usage Guide

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

## ⚙️ Configuration Reference

The CLI and Client resolve configuration in the following order:

1.  **CLI Arguments** (`--api-key`, `--location-id`)
2.  **Environment Variables** (`GHL_API_KEY`, `GHL_LOCATION_ID`)
3.  **Config File** (`~/.config/ghl/config.json`)

## ⚠️ Error Handling & Retries

The client uses `httpx` and raises `httpx.HTTPStatusError` for 4xx/5xx responses. The error message is enriched with details from the API response.

```python
import httpx
from ghl.endpoints import contacts

try:
    contacts.get_contact(client, "invalid_id")
except httpx.HTTPStatusError as e:
    print(f"Error: {e}")
    # e.response.json() contains API error details
```

**Automatic Token Refresh:**
If `client_id`, `client_secret`, and `refresh_token` are provided to `GHLClient`, it will automatically attempt to refresh the access token on 401 Unauthorized errors and retry the request.

## 🧪 Testing

To run the tests, you need to set the `PYTHONPATH` to include the source directory.

```bash
cd wrapper
PYTHONPATH=src pytest tests/
```

## 🤖 AI Manual

For AI agents using this library, please refer to the [AI Manual](docs/AI-MANUAL.md) for optimized patterns and structured references.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1.  Fork the repository.
2.  Create a feature branch.
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.

## 📄 License

This project is licensed under the MIT License.
