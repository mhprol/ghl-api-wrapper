# GoHighLevel API CLI Wrapper

A Python CLI wrapper for the GoHighLevel (GHL) API v2.

## Installation

```bash
cd wrapper
pip install -e .
```

## Configuration

You can configure the CLI using environment variables, a config file, or command-line arguments.

### Environment Variables

```bash
export GHL_API_KEY="your_api_key"
export GHL_LOCATION_ID="your_location_id"
```

### Config File

Create `~/.config/ghl/config.json`:

```json
{
  "api_key": "your_api_key",
  "location_id": "your_location_id"
}
```

### Command Line Arguments

```bash
ghl --api-key "your_api_key" --location-id "your_location_id" ...
```

## Usage

### Contacts

```bash
# List contacts
ghl contacts list --limit 10

# Search contacts
ghl contacts search --query "john"

# Get contact
ghl contacts get <contact_id>

# Create contact
ghl contacts create --data '{"firstName": "John", "lastName": "Doe", "email": "john@example.com"}'

# Update contact
ghl contacts update <contact_id> --data '{"phone": "+1234567890"}'

# Delete contact
ghl contacts delete <contact_id>
```

### Conversations

```bash
# List conversations
ghl conversations list --status unread

# Get conversation
ghl conversations get <conversation_id>

# Get messages
ghl conversations messages <conversation_id>
```

### Opportunities

```bash
# List opportunities
ghl opportunities list --status open

# Get opportunity
ghl opportunities get <opportunity_id>

# List pipelines
ghl opportunities pipelines
```

### Calendars

```bash
# List calendars
ghl calendars list

# List events
ghl calendars events --start-time 1600000000000 --end-time 1700000000000
```

### Workflows

```bash
# List workflows
ghl workflows list
```

### Custom Objects

```bash
# List object schemas
ghl objects list-schemas

# Get object schema
ghl objects get-schema custom_objects.pet

# List records
ghl objects list custom_objects.pet

# Get record
ghl objects get custom_objects.pet <record_id>

# Create record
ghl objects create custom_objects.pet --data '{"properties": {"name": "Buddy"}}'
```

### Locations (Sub-accounts)

```bash
# List locations
ghl locations list --limit 5

# Get location
ghl locations get <location_id>
```

## Development

Run tests:

```bash
pytest
```
