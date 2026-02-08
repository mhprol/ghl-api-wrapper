# GHL API Wrapper AI Manual

**Design Principle:** Progressive Disclosure - Structured so an AI agent loads ONLY what it needs.

## Level 1 - Quick Reference

| Intent | Module | Command | Example |
| :--- | :--- | :--- | :--- |
| **Contacts** | | | |
| List Contacts | `contacts` | `list` | `ghl contacts list --limit 5` |
| Get Contact | `contacts` | `get` | `ghl contacts get <id>` |
| Create Contact | `contacts` | `create` | `ghl contacts create --data '{"email": "test@example.com"}'` |
| Update Contact | `contacts` | `update` | `ghl contacts update <id> --data '{"firstName": "John"}'` |
| Delete Contact | `contacts` | `delete` | `ghl contacts delete <id>` |
| Search Contacts | `contacts` | `search` | `ghl contacts search --query "email:*@example.com"` |
| **Conversations** | | | |
| List Conversations | `conversations` | `list` | `ghl conversations list --status unread` |
| Get Conversation | `conversations` | `get` | `ghl conversations get <id>` |
| Create Conversation | `conversations` | `create` | `ghl conversations create --data '{"contactId": "..."}'` |
| Update Conversation | `conversations` | `update` | `ghl conversations update <id> --data '{"status": "read"}'` |
| Delete Conversation | `conversations` | `delete` | `ghl conversations delete <id>` |
| Get Messages | `conversations` | `messages` | `ghl conversations messages <id> --limit 10` |
| **Calendars** | | | |
| List Calendars | `calendars` | `list` | `ghl calendars list` |
| Get Calendar | `calendars` | `get` | `ghl calendars get <id>` |
| Create Calendar | `calendars` | `create` | `ghl calendars create --data '{"name": "Demo"}'` |
| Update Calendar | `calendars` | `update` | `ghl calendars update <id> --data '{"name": "New Name"}'` |
| Delete Calendar | `calendars` | `delete` | `ghl calendars delete <id>` |
| List Events | `calendars` | `events` | `ghl calendars events --start-time 12345 --end-time 67890` |
| **Workflows** | | | |
| List Workflows | `workflows` | `list` | `ghl workflows list` |
| **Opportunities** | | | |
| List Opportunities | `opportunities` | `list` | `ghl opportunities list --status open` |
| Get Opportunity | `opportunities` | `get` | `ghl opportunities get <id>` |
| Create Opportunity | `opportunities` | `create` | `ghl opportunities create --data '{"pipelineId": "..."}'` |
| Update Opportunity | `opportunities` | `update` | `ghl opportunities update <id> --data '{"status": "won"}'` |
| Delete Opportunity | `opportunities` | `delete` | `ghl opportunities delete <id>` |
| List Pipelines | `opportunities` | `pipelines` | `ghl opportunities pipelines` |
| **Locations** | | | |
| List Locations | `locations` | `list` | `ghl locations list --limit 10` |
| Get Location | `locations` | `get` | `ghl locations get <id>` |
| Create Location | `locations` | `create` | `ghl locations create --data '{"name": "New Loc"}'` |
| Update Location | `locations` | `update` | `ghl locations update <id> --data '{"email": "..."}'` |
| Delete Location | `locations` | `delete` | `ghl locations delete <id>` |
| **Custom Objects** | | | |
| List Schemas | `objects` | `list-schemas` | `ghl objects list-schemas` |
| Get Schema | `objects` | `get-schema` | `ghl objects get-schema <key>` |
| List Records | `objects` | `list` | `ghl objects list <schema_key>` |
| Get Record | `objects` | `get` | `ghl objects get <schema_key> <id>` |
| Create Record | `objects` | `create` | `ghl objects create <schema_key> --data '{"properties": ...}'` |
| Update Record | `objects` | `update` | `ghl objects update <schema_key> <id> --data '{"properties": ...}'` |
| Delete Record | `objects` | `delete` | `ghl objects delete <schema_key> <id>` |

## Level 2 - Detailed Usage

### Contacts Module

**List Contacts**
`ghl contacts list [OPTIONS]`
- `--limit INT`: Max results (default 20).
- `--query STR`: Search term (name, email, phone).
- `--fields STR`: Comma-separated fields to return (e.g., "id,email,phone").
- `-v`: Verbose mode (level 1 adds common fields, level 2 adds all fields).

**Get Contact**
`ghl contacts get CONTACT_ID [OPTIONS]`
- `--fields STR`: Specific fields to return.
- `-v`: Verbose mode.

**Create Contact**
`ghl contacts create --data JSON_STR`
Payload:
```json
{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1234567890",
  "tags": ["lead", "ai-generated"],
  "customFields": {
    "field_id": "value"
  }
}
```

**Update Contact**
`ghl contacts update CONTACT_ID --data JSON_STR`
Payload: partial object.
```json
{
  "email": "new.email@example.com",
  "tags": ["updated"]
}
```

**Delete Contact**
`ghl contacts delete CONTACT_ID`

**Search Contacts**
`ghl contacts search --query STR [OPTIONS]`
- Alias for `list` with a required query parameter.
- Supports simple string matching.

### Conversations Module

**List Conversations**
`ghl conversations list [OPTIONS]`
- `--limit INT`: Max results (default 20).
- `--query STR`: Search by contact name, email, or phone.
- `--status STR`: Filter by status (`all`, `read`, `unread`, `starred`, `recents`).

**Get Conversation**
`ghl conversations get CONVERSATION_ID`

**Create Conversation**
`ghl conversations create --data JSON_STR`
Payload:
```json
{
  "contactId": "CONTACT_ID_HERE",
  "locationId": "LOCATION_ID_HERE",
  "inbound": true,
  "type": "SMS"
}
```
Types: `SMS`, `EMAIL`, `WHATSAPP`, `GMB`, `FACEBOOK`, `INSTAGRAM`.

**Update Conversation**
`ghl conversations update CONVERSATION_ID --data JSON_STR`
Payload:
```json
{
  "status": "read",
  "unreadCount": 0,
  "starred": true
}
```

**Delete Conversation**
`ghl conversations delete CONVERSATION_ID`

**Get Messages**
`ghl conversations messages CONVERSATION_ID --limit INT`
- Returns list of messages in the conversation.

### Calendars Module

**List Calendars**
`ghl calendars list [OPTIONS]`
- `--group-id STR`: Filter by calendar group ID.

**Get Calendar**
`ghl calendars get CALENDAR_ID`

**Create Calendar**
`ghl calendars create --data JSON_STR`
Payload:
```json
{
  "name": "Consultation",
  "description": "Initial consult",
  "slug": "consult",
  "eventType": "round_robin"
}
```

**Update Calendar**
`ghl calendars update CALENDAR_ID --data JSON_STR`

**Delete Calendar**
`ghl calendars delete CALENDAR_ID`

**List Events**
`ghl calendars events --start-time INT --end-time INT [OPTIONS]`
- `--start-time`: Start timestamp (epoch millis).
- `--end-time`: End timestamp (epoch millis).
- `--calendar-id STR`: Filter by calendar.

### Workflows Module

**List Workflows**
`ghl workflows list`
- Lists all workflows for the current location.

### Opportunities Module

**List Opportunities**
`ghl opportunities list [OPTIONS]`
- `--limit INT`: Max results (default 20).
- `--query STR`: Search query.
- `--pipeline-id STR`: Filter by pipeline.
- `--status STR`: Filter by status (`open`, `won`, `lost`, `abandoned`, `all`).

**Get Opportunity**
`ghl opportunities get OPPORTUNITY_ID`

**Create Opportunity**
`ghl opportunities create --data JSON_STR`
Payload:
```json
{
  "pipelineId": "PIPELINE_ID",
  "locationId": "LOCATION_ID",
  "contactId": "CONTACT_ID",
  "name": "Deal Name",
  "status": "open",
  "stageId": "STAGE_ID",
  "monetaryValue": 1000
}
```

**Update Opportunity**
`ghl opportunities update OPPORTUNITY_ID --data JSON_STR`
Payload: partial object.
```json
{
  "status": "won",
  "monetaryValue": 1200
}
```

**Delete Opportunity**
`ghl opportunities delete OPPORTUNITY_ID`

**List Pipelines**
`ghl opportunities pipelines`
- Returns pipelines and their stages. Useful for getting `pipelineId` and `stageId` for opportunity creation.

### Locations Module

**List Locations**
`ghl locations list [OPTIONS]`
- `--limit INT`: Max results (default 10).
- `--skip INT`: Skip count.
- `--email STR`: Filter by email.
- `--company-id STR`: Filter by company.

**Get Location**
`ghl locations get LOCATION_ID`

**Create Location**
`ghl locations create --data JSON_STR`
Payload:
```json
{
  "name": "New Branch",
  "email": "branch@example.com",
  "phone": "+1234567890",
  "address": "123 Main St",
  "city": "City",
  "state": "State",
  "country": "US",
  "postalCode": "12345",
  "website": "https://example.com",
  "timezone": "US/Pacific"
}
```

**Update Location**
`ghl locations update LOCATION_ID --data JSON_STR`
Payload: partial object.

**Delete Location**
`ghl locations delete LOCATION_ID [OPTIONS]`
- `--delete-twilio-account`: Flag to delete associated Twilio account.

### Custom Objects Module

**List Schemas**
`ghl objects list-schemas`
- Lists all available custom object schemas (keys).

**Get Schema**
`ghl objects get-schema SCHEMA_KEY`
- Returns the definition of a specific custom object (fields, relations).

**List Records**
`ghl objects list SCHEMA_KEY [OPTIONS]`
- `--limit INT`: Max results.
- `--query STR`: Search query.

**Get Record**
`ghl objects get SCHEMA_KEY RECORD_ID`

**Create Record**
`ghl objects create SCHEMA_KEY --data JSON_STR`
Payload:
```json
{
  "properties": {
    "custom_field_key": "value",
    "another_field": 123
  }
}
```

**Update Record**
`ghl objects update SCHEMA_KEY RECORD_ID --data JSON_STR`
Payload: partial object in `properties`.

**Delete Record**
`ghl objects delete SCHEMA_KEY RECORD_ID`

## Level 3 - Patterns and Combinations

### 1. Contact Lookup & Engagement
**Scenario:** Find a contact by email and start a conversation.
1. Search for contact:
   `contact = ghl contacts search --query "test@example.com"`
2. Extract `contact.id`.
3. Create conversation:
   `ghl conversations create --data '{"contactId": "'"$CONTACT_ID"'", "type": "SMS", "inbound": false}'`

### 2. Opportunity Pipeline Progression
**Scenario:** Move a lead to "Negotiation" stage.
1. List pipelines to get IDs:
   `ghl opportunities pipelines`
   (Find `pipelineId` and target `stageId`).
2. Update opportunity:
   `ghl opportunities update OPPORTUNITY_ID --data '{"stageId": "TARGET_STAGE_ID", "status": "open"}'`

### 3. Calendar Booking
**Scenario:** Book a consultation for a contact.
1. Ensure contact exists (get ID).
2. Create event:
   ```json
   {
     "calendarId": "CALENDAR_ID",
     "locationId": "LOCATION_ID",
     "contactId": "CONTACT_ID",
     "startTime": "2023-10-27T10:00:00-07:00",
     "endTime": "2023-10-27T11:00:00-07:00",
     "title": "Consultation",
     "meetingStatus": "confirmed"
   }
   ```
   Note: Use ISO 8601 strings or epoch millis depending on specific endpoint nuances (wrapper handles some conversions, but raw JSON passes through).

### 4. Workflow Triggering
**Scenario:** Trigger a workflow manually (if supported) or via tag.
- GHL API often triggers workflows via "Contact Tag Added".
- Add tag:
  `ghl contacts update CONTACT_ID --data '{"tags": ["trigger-welcome-sequence"]}'`

### 5. Custom Object State Tracking
**Scenario:** Store external app state (e.g., Zaptos sync status) on a contact-linked custom object.
1. Define Custom Object Schema `zaptos_sync`.
2. Create record linked to contact:
   ```json
   {
     "properties": {
       "contact_id": "CONTACT_ID",
       "last_sync": "2023-10-27",
       "status": "synced"
     }
   }
   ```

### 6. Pagination Pattern
**Scenario:** Fetch all contacts.
- Loop while results < total:
  `ghl contacts list --limit 100 --skip 0`
  `ghl contacts list --limit 100 --skip 100`
  (Note: `contacts list` in CLI currently uses limit/query. Pagination via `searchAfter` or `skip` depends on specific endpoint implementation. Check `meta` response).

## Critical Notes

### Authentication
- **Environment Variables:** `GHL_API_KEY` and `GHL_LOCATION_ID` are primary.
- **Profile:** Use `--profile` to switch between configs in `~/.config/ghl/profiles.yaml`.

### Multi-Tenant Support
- The wrapper supports managing multiple locations.
- Switch context using `--location-id` flag on any command to override the default.
- `ghl locations create` allows agency-level creation of sub-accounts.

### Data Formats
- **Phone Numbers:** Strict E.164 format required (e.g., `+15551234567`, `+5511999999999`).
- **Dates:** ISO 8601 preferred for JSON payloads. Timestamps (epoch millis) for query parameters like `--start-time`.

### Rate Limits & Reliability
- GHL API has rate limits (approx 100 requests/10 sec per location).
- Implement exponential backoff for `429 Too Many Requests`.
- The CLI wrapper handles standard HTTP errors but does not auto-retry 429s effectively in all cases—agent should handle retries.
