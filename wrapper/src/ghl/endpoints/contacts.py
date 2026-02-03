from typing import Optional, Dict, Any, List
from ..client import GHLClient

ESSENTIAL_FIELDS = ["id", "email", "name", "firstName", "lastName"]
COMMON_FIELDS = ESSENTIAL_FIELDS + ["phone", "tags", "source", "dateAdded"]

def _filter_fields(data: Any, fields: Optional[str], verbose: int) -> Any:
    if isinstance(data, list):
        return [_filter_fields(item, fields, verbose) for item in data]

    if not isinstance(data, dict):
        return data

    if fields:
        selected = fields.split(",")
    elif verbose >= 2:
        return data # All fields
    elif verbose == 1:
        selected = COMMON_FIELDS
    else:
        selected = ESSENTIAL_FIELDS

    return {k: data.get(k) for k in selected if k in data}

def list_contacts(client: GHLClient, limit: int = 20, query: Optional[str] = None, fields: Optional[str] = None, verbose: int = 0) -> Dict[str, Any]:
    params = {"limit": limit}
    if query:
        params["query"] = query

    response = client.get("/contacts/", params=params)
    response.raise_for_status()
    data = response.json()

    contacts = data.get("contacts", [])
    filtered_contacts = _filter_fields(contacts, fields, verbose)

    return {"contacts": filtered_contacts, "meta": data.get("meta", {})}

def get_contact(client: GHLClient, contact_id: str, fields: Optional[str] = None, verbose: int = 0) -> Dict[str, Any]:
    response = client.get(f"/contacts/{contact_id}")
    response.raise_for_status()
    data = response.json()

    contact = data.get("contact", {})
    return _filter_fields(contact, fields, verbose)

def create_contact(client: GHLClient, data: Dict[str, Any]) -> Dict[str, Any]:
    response = client.post("/contacts/", json=data)
    response.raise_for_status()
    return response.json()

def update_contact(client: GHLClient, contact_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    response = client.put(f"/contacts/{contact_id}", json=data)
    response.raise_for_status()
    return response.json()

def delete_contact(client: GHLClient, contact_id: str) -> Dict[str, Any]:
    response = client.delete(f"/contacts/{contact_id}")
    response.raise_for_status()
    return response.json()

def search_contacts(client: GHLClient, query: str, fields: Optional[str] = None, verbose: int = 0) -> Dict[str, Any]:
    # Delegating to list_contacts as the GET /contacts/ endpoint supports a query parameter
    # which effectively acts as a search.
    return list_contacts(client, limit=100, query=query, fields=fields, verbose=verbose)
