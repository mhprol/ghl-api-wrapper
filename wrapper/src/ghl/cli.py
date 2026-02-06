import click
import json
import sys
from .config import get_config
from .client import GHLClient
from .endpoints import contacts, conversations, opportunities, calendars, workflows, objects, locations

@click.group()
@click.option('--api-key', help='API Key for GHL (or set GHL_API_KEY)')
@click.option('--location-id', help='Location ID for GHL (or set GHL_LOCATION_ID)')
@click.option('--profile', help='Use named profile from profiles.yaml')
@click.pass_context
def cli(ctx, api_key, location_id, profile):
    """GoHighLevel CLI Wrapper"""
    ctx.ensure_object(dict)

    config = get_config(api_key, location_id, profile)
    final_api_key = config.get("api_key")
    final_location_id = config.get("location_id")

    if final_api_key:
        ctx.obj['client'] = GHLClient(final_api_key, final_location_id)
    else:
         ctx.obj['client'] = None

# Contacts Group
@cli.group()
def contacts_group():
    """Contact management"""
    pass

@contacts_group.command('list')
@click.option('--limit', default=20, help='Limit number of results')
@click.option('--query', default=None, help='Search query')
@click.option('--fields', default=None, help='Comma-separated fields to include')
@click.option('-v', '--verbose', count=True, help='Verbosity level')
@click.pass_context
def contacts_list(ctx, limit, query, fields, verbose):
    """List contacts"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = contacts.list_contacts(client, limit, query, fields, verbose)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@contacts_group.command('get')
@click.argument('contact_id')
@click.option('--fields', default=None, help='Comma-separated fields to include')
@click.option('-v', '--verbose', count=True, help='Verbosity level')
@click.pass_context
def contacts_get(ctx, contact_id, fields, verbose):
    """Get a contact by ID"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = contacts.get_contact(client, contact_id, fields, verbose)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@contacts_group.command('create')
@click.option('--data', help='JSON data for creation')
@click.option('--file', type=click.File('r'), help='JSON file for creation')
@click.pass_context
def contacts_create(ctx, data, file):
    """Create a contact"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    if data:
        payload = json.loads(data)
    elif file:
        payload = json.load(file)
    else:
        click.echo("Error: Must provide --data or --file", err=True)
        sys.exit(1)

    try:
        result = contacts.create_contact(client, payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@contacts_group.command('update')
@click.argument('contact_id')
@click.option('--data', required=True, help='JSON data for update')
@click.pass_context
def contacts_update(ctx, contact_id, data):
    """Update a contact"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        payload = json.loads(data)
        result = contacts.update_contact(client, contact_id, payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@contacts_group.command('delete')
@click.argument('contact_id')
@click.pass_context
def contacts_delete(ctx, contact_id):
    """Delete a contact"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = contacts.delete_contact(client, contact_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@contacts_group.command('search')
@click.option('--query', required=True, help='Search query')
@click.option('--fields', default=None, help='Comma-separated fields to include')
@click.option('-v', '--verbose', count=True, help='Verbosity level')
@click.pass_context
def contacts_search(ctx, query, fields, verbose):
    """Search contacts"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        # Re-using list_contacts logic for now as search_contacts was stubbed
        # If I want to implement search_contacts properly I need to update contacts.py
        result = contacts.list_contacts(client, limit=100, query=query, fields=fields, verbose=verbose)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

cli.add_command(contacts_group, name='contacts')

# Conversations Group
@cli.group()
def conversations_group():
    """Conversation management"""
    pass

@conversations_group.command('list')
@click.option('--limit', default=20, help='Limit number of results')
@click.option('--query', default=None, help='Search query')
@click.option('--status', default=None, help='Filter by status (all, read, unread, starred, recents)')
@click.pass_context
def conversations_list(ctx, limit, query, status):
    """List conversations"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = conversations.list_conversations(client, limit, query, status)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@conversations_group.command('get')
@click.argument('conversation_id')
@click.pass_context
def conversations_get(ctx, conversation_id):
    """Get a conversation by ID"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = conversations.get_conversation(client, conversation_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@conversations_group.command('create')
@click.option('--data', help='JSON data for creation')
@click.option('--file', type=click.File('r'), help='JSON file for creation')
@click.pass_context
def conversations_create(ctx, data, file):
    """Create a conversation"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    if data:
        payload = json.loads(data)
    elif file:
        payload = json.load(file)
    else:
        click.echo("Error: Must provide --data or --file", err=True)
        sys.exit(1)

    try:
        result = conversations.create_conversation(client, payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@conversations_group.command('update')
@click.argument('conversation_id')
@click.option('--data', required=True, help='JSON data for update')
@click.pass_context
def conversations_update(ctx, conversation_id, data):
    """Update a conversation"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        payload = json.loads(data)
        result = conversations.update_conversation(client, conversation_id, payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@conversations_group.command('delete')
@click.argument('conversation_id')
@click.pass_context
def conversations_delete(ctx, conversation_id):
    """Delete a conversation"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = conversations.delete_conversation(client, conversation_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@conversations_group.command('messages')
@click.argument('conversation_id')
@click.option('--limit', default=20, help='Limit number of messages')
@click.pass_context
def conversations_messages(ctx, conversation_id, limit):
    """Get messages for a conversation"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = conversations.get_messages(client, conversation_id, limit)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

cli.add_command(conversations_group, name='conversations')

# Opportunities Group
@cli.group()
def opportunities_group():
    """Opportunity management"""
    pass

@opportunities_group.command('list')
@click.option('--limit', default=20, help='Limit number of results')
@click.option('--query', default=None, help='Search query')
@click.option('--pipeline-id', default=None, help='Filter by pipeline ID')
@click.option('--status', default=None, help='Filter by status (open, won, lost, abandoned, all)')
@click.pass_context
def opportunities_list(ctx, limit, query, pipeline_id, status):
    """List opportunities"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = opportunities.list_opportunities(client, limit, query, pipeline_id, status)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@opportunities_group.command('get')
@click.argument('opportunity_id')
@click.pass_context
def opportunities_get(ctx, opportunity_id):
    """Get an opportunity by ID"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = opportunities.get_opportunity(client, opportunity_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@opportunities_group.command('create')
@click.option('--data', help='JSON data for creation')
@click.option('--file', type=click.File('r'), help='JSON file for creation')
@click.pass_context
def opportunities_create(ctx, data, file):
    """Create an opportunity"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    if data:
        payload = json.loads(data)
    elif file:
        payload = json.load(file)
    else:
        click.echo("Error: Must provide --data or --file", err=True)
        sys.exit(1)

    try:
        result = opportunities.create_opportunity(client, payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@opportunities_group.command('update')
@click.argument('opportunity_id')
@click.option('--data', required=True, help='JSON data for update')
@click.pass_context
def opportunities_update(ctx, opportunity_id, data):
    """Update an opportunity"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        payload = json.loads(data)
        result = opportunities.update_opportunity(client, opportunity_id, payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@opportunities_group.command('delete')
@click.argument('opportunity_id')
@click.pass_context
def opportunities_delete(ctx, opportunity_id):
    """Delete an opportunity"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = opportunities.delete_opportunity(client, opportunity_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@opportunities_group.command('pipelines')
@click.pass_context
def opportunities_pipelines(ctx):
    """List pipelines"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = opportunities.list_pipelines(client)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

cli.add_command(opportunities_group, name='opportunities')

# Calendars Group
@cli.group()
def calendars_group():
    """Calendar management"""
    pass

@calendars_group.command('list')
@click.option('--group-id', default=None, help='Filter by group ID')
@click.pass_context
def calendars_list(ctx, group_id):
    """List calendars"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = calendars.list_calendars(client, group_id=group_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@calendars_group.command('get')
@click.argument('calendar_id')
@click.pass_context
def calendars_get(ctx, calendar_id):
    """Get a calendar by ID"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = calendars.get_calendar(client, calendar_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@calendars_group.command('create')
@click.option('--data', help='JSON data for creation')
@click.option('--file', type=click.File('r'), help='JSON file for creation')
@click.pass_context
def calendars_create(ctx, data, file):
    """Create a calendar"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    if data:
        payload = json.loads(data)
    elif file:
        payload = json.load(file)
    else:
        click.echo("Error: Must provide --data or --file", err=True)
        sys.exit(1)

    try:
        result = calendars.create_calendar(client, payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@calendars_group.command('update')
@click.argument('calendar_id')
@click.option('--data', required=True, help='JSON data for update')
@click.pass_context
def calendars_update(ctx, calendar_id, data):
    """Update a calendar"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        payload = json.loads(data)
        result = calendars.update_calendar(client, calendar_id, payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@calendars_group.command('delete')
@click.argument('calendar_id')
@click.pass_context
def calendars_delete(ctx, calendar_id):
    """Delete a calendar"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = calendars.delete_calendar(client, calendar_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@calendars_group.command('events')
@click.option('--start-time', required=True, help='Start time (millis)')
@click.option('--end-time', required=True, help='End time (millis)')
@click.option('--calendar-id', default=None, help='Filter by calendar ID')
@click.pass_context
def calendars_events(ctx, start_time, end_time, calendar_id):
    """List calendar events"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = calendars.list_events(client, start_time, end_time, calendar_id=calendar_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

cli.add_command(calendars_group, name='calendars')

# Workflows Group
@cli.group()
def workflows_group():
    """Workflow management"""
    pass

@workflows_group.command('list')
@click.pass_context
def workflows_list(ctx):
    """List workflows"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = workflows.list_workflows(client)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

cli.add_command(workflows_group, name='workflows')

# Objects Group
@cli.group()
def objects_group():
    """Custom Object management"""
    pass

@objects_group.command('list-schemas')
@click.pass_context
def objects_list_schemas(ctx):
    """List object schemas"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = objects.list_schemas(client)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@objects_group.command('get-schema')
@click.argument('key')
@click.pass_context
def objects_get_schema(ctx, key):
    """Get object schema by key"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = objects.get_schema(client, key)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@objects_group.command('list')
@click.argument('schema_key')
@click.option('--limit', default=20, help='Limit number of results')
@click.option('--query', default=None, help='Search query')
@click.pass_context
def objects_list_records(ctx, schema_key, limit, query):
    """List records for a schema"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = objects.list_records(client, schema_key, limit, query)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@objects_group.command('get')
@click.argument('schema_key')
@click.argument('record_id')
@click.pass_context
def objects_get_record(ctx, schema_key, record_id):
    """Get a record by ID"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = objects.get_record(client, schema_key, record_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@objects_group.command('create')
@click.argument('schema_key')
@click.option('--data', help='JSON data for creation')
@click.option('--file', type=click.File('r'), help='JSON file for creation')
@click.pass_context
def objects_create_record(ctx, schema_key, data, file):
    """Create a record"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    if data:
        payload = json.loads(data)
    elif file:
        payload = json.load(file)
    else:
        click.echo("Error: Must provide --data or --file", err=True)
        sys.exit(1)

    try:
        result = objects.create_record(client, schema_key, payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@objects_group.command('update')
@click.argument('schema_key')
@click.argument('record_id')
@click.option('--data', required=True, help='JSON data for update')
@click.pass_context
def objects_update_record(ctx, schema_key, record_id, data):
    """Update a record"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        payload = json.loads(data)
        result = objects.update_record(client, schema_key, record_id, payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@objects_group.command('delete')
@click.argument('schema_key')
@click.argument('record_id')
@click.pass_context
def objects_delete_record(ctx, schema_key, record_id):
    """Delete a record"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = objects.delete_record(client, schema_key, record_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

cli.add_command(objects_group, name='objects')

# Locations Group
@cli.group()
def locations_group():
    """Location (Sub-account) management"""
    pass

@locations_group.command('list')
@click.option('--limit', default=10, help='Limit number of results')
@click.option('--skip', default=0, help='Skip number of results')
@click.option('--email', default=None, help='Filter by email')
@click.option('--company-id', default=None, help='Filter by company ID')
@click.pass_context
def locations_list(ctx, limit, skip, email, company_id):
    """List locations"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = locations.list_locations(client, limit, skip, email, company_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@locations_group.command('get')
@click.argument('location_id')
@click.pass_context
def locations_get(ctx, location_id):
    """Get a location by ID"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = locations.get_location(client, location_id)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@locations_group.command('create')
@click.option('--data', help='JSON data for creation')
@click.option('--file', type=click.File('r'), help='JSON file for creation')
@click.pass_context
def locations_create(ctx, data, file):
    """Create a location"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    if data:
        payload = json.loads(data)
    elif file:
        payload = json.load(file)
    else:
        click.echo("Error: Must provide --data or --file", err=True)
        sys.exit(1)

    try:
        result = locations.create_location(client, payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@locations_group.command('update')
@click.argument('location_id')
@click.option('--data', required=True, help='JSON data for update')
@click.pass_context
def locations_update(ctx, location_id, data):
    """Update a location"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        payload = json.loads(data)
        result = locations.update_location(client, location_id, payload)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

@locations_group.command('delete')
@click.argument('location_id')
@click.option('--delete-twilio-account', is_flag=True, help='Delete associated Twilio account')
@click.pass_context
def locations_delete(ctx, location_id, delete_twilio_account):
    """Delete a location"""
    client = ctx.obj['client']
    if not client:
        click.echo("Error: API Key is missing.", err=True)
        sys.exit(1)

    try:
        result = locations.delete_location(client, location_id, delete_twilio_account)
        click.echo(json.dumps(result, indent=2))
    except Exception as e:
        click.echo(json.dumps({"error": str(e)}), err=True)
        sys.exit(1)

cli.add_command(locations_group, name='locations')

if __name__ == '__main__':
    cli()
