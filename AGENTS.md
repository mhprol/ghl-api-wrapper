# AGENTS.md — GHL API Wrapper

## Project Overview

Build a Python CLI wrapper for the GoHighLevel (GHL) API v2. This repo is a fork of `GoHighLevel/highlevel-api-docs` with an added `wrapper/` directory containing the CLI tool.

## Architecture

```
ghl-api-wrapper/
├── docs/                        # (upstream) API documentation
├── models/                      # (upstream) Data models  
├── apps/                        # (upstream) Apps docs
├── toc.json                     # (upstream) Table of contents
├── wrapper/                     # NEW: Our CLI wrapper
│   ├── ghl                      # Main CLI entrypoint (executable)
│   ├── pyproject.toml           # Python project config (uv/pip)
│   ├── src/
│   │   └── ghl/
│   │       ├── __init__.py
│   │       ├── cli.py           # CLI argument parsing
│   │       ├── client.py        # HTTP client base
│   │       ├── config.py        # API key management
│   │       └── endpoints/       # One file per resource
│   │           ├── __init__.py
│   │           ├── contacts.py
│   │           ├── conversations.py
│   │           ├── opportunities.py
│   │           ├── calendars.py
│   │           ├── workflows.py
│   │           ├── objects.py   # Custom Objects
│   │           └── locations.py
│   └── tests/
│       └── ...
└── AGENTS.md                    # This file
```

## CLI Design

### Command Structure

```bash
ghl <resource> <action> [options]
```

### Resources (Priority Order)

1. **contacts** — Contact management
2. **conversations** — Messages and threads
3. **opportunities** — Pipeline and deals
4. **calendars** — Appointments and availability
5. **workflows** — Automation triggers
6. **objects** — Custom Objects CRUD
7. **locations** — Location/sub-account management

### Actions (per resource)

```bash
ghl contacts list [--limit N] [--query Q] [--fields F]
ghl contacts get <id> [--fields F] [-v|-vv]
ghl contacts create --data '{...}' | --file data.json
ghl contacts update <id> --data '{...}'
ghl contacts delete <id>
ghl contacts search --query "email:*@example.com"
```

### Global Options

```bash
--api-key KEY      # Override env GHL_API_KEY
--location-id ID   # Override env GHL_LOCATION_ID  
--output json      # Always JSON (default)
--fields F1,F2     # Select specific fields
-v, -vv            # Verbosity (more fields)
--dry-run          # Show request without executing
--debug            # Show HTTP details
```

### Authentication

API Key via:
1. `--api-key` flag
2. `GHL_API_KEY` environment variable
3. `~/.config/ghl/config.json`

Location ID via:
1. `--location-id` flag
2. `GHL_LOCATION_ID` environment variable
3. Config file

### Output

Always JSON to stdout. Errors to stderr.

```bash
# Success
{"contacts": [...], "meta": {"total": 100, "count": 10}}

# Error
{"error": "Not found", "code": 404, "details": {...}}
```

### Progressive Disclosure

```bash
# Default: essential fields only
ghl contacts get abc123
# {"id": "abc123", "email": "x@y.com", "name": "John"}

# Verbose: + common fields
ghl contacts get abc123 -v
# {"id": "...", "email": "...", "name": "...", "phone": "...", "tags": [...]}

# Very verbose: all fields
ghl contacts get abc123 -vv
# Full API response

# Explicit field selection
ghl contacts get abc123 --fields=email,phone,customFields
```

## Implementation Notes

### HTTP Client

Use `httpx` for async-capable HTTP:

```python
import httpx

class GHLClient:
    BASE_URL = "https://services.leadconnectorhq.com"
    
    def __init__(self, api_key: str, location_id: str = None):
        self.api_key = api_key
        self.location_id = location_id
        self.client = httpx.Client(
            base_url=self.BASE_URL,
            headers={"Authorization": f"Bearer {api_key}"}
        )
```

### Endpoint Pattern

Each endpoint file follows this pattern:

```python
# endpoints/contacts.py
from ..client import GHLClient

ESSENTIAL_FIELDS = ["id", "email", "name", "firstName", "lastName"]
COMMON_FIELDS = ESSENTIAL_FIELDS + ["phone", "tags", "source", "dateAdded"]

def list_contacts(client: GHLClient, limit=20, query=None, fields=None, verbose=0):
    params = {"limit": limit}
    if query:
        params["query"] = query
    
    response = client.get(f"/contacts/", params=params)
    contacts = response.json().get("contacts", [])
    
    # Apply field filtering based on verbosity
    if fields:
        selected = fields.split(",")
    elif verbose >= 2:
        selected = None  # All fields
    elif verbose == 1:
        selected = COMMON_FIELDS
    else:
        selected = ESSENTIAL_FIELDS
    
    if selected:
        contacts = [{k: c.get(k) for k in selected if k in c} for c in contacts]
    
    return {"contacts": contacts, "meta": response.json().get("meta", {})}
```

### CLI Entry Point

Use `click` for CLI:

```python
# cli.py
import click
import json
from .config import get_config
from .client import GHLClient
from .endpoints import contacts, conversations, ...

@click.group()
@click.option('--api-key', envvar='GHL_API_KEY')
@click.option('--location-id', envvar='GHL_LOCATION_ID')
@click.pass_context
def cli(ctx, api_key, location_id):
    ctx.ensure_object(dict)
    ctx.obj['client'] = GHLClient(api_key, location_id)

@cli.group()
def contacts():
    """Contact management"""
    pass

@contacts.command('list')
@click.option('--limit', default=20)
@click.option('--query', default=None)
@click.option('--fields', default=None)
@click.option('-v', '--verbose', count=True)
@click.pass_context
def contacts_list(ctx, limit, query, fields, verbose):
    result = contacts.list_contacts(ctx.obj['client'], limit, query, fields, verbose)
    click.echo(json.dumps(result, indent=2))
```

## API Reference

Use the docs in this repo (`docs/`, `models/`) as the source of truth for:
- Endpoint URLs
- Request/response schemas
- Required vs optional parameters
- Error codes

Key docs:
- `docs/contacts/` — Contact endpoints
- `docs/conversations/` — Messaging
- `docs/opportunities/` — Pipeline
- `docs/calendars/` — Scheduling
- `docs/workflows/` — Automation
- `docs/objects/` or `apps/objects/` — Custom Objects
- `docs/locations/` — Sub-accounts

## Testing

Create basic tests for each endpoint:

```python
# tests/test_contacts.py
def test_list_contacts():
    # Mock or use test API key
    pass
```

## Deliverables

1. Working CLI with all 7 resources
2. Each resource supports: list, get, create, update, delete (where applicable)
3. Field selection and verbosity working
4. Config file support
5. Basic error handling
6. README with usage examples

## Priority

Implement in this order:
1. Core client + config + CLI skeleton
2. contacts (most used)
3. conversations
4. opportunities  
5. calendars
6. workflows
7. objects (Custom Objects)
8. locations

## Style

- Python 3.11+
- Type hints everywhere
- Use `ruff` for linting
- Use `uv` or `pip` for deps
- Minimal dependencies: `click`, `httpx`, `pydantic` (optional)
