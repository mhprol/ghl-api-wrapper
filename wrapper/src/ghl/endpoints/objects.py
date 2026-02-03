from typing import Optional, Dict, Any
from ..client import GHLClient

def list_schemas(client: GHLClient, location_id: Optional[str] = None) -> Dict[str, Any]:
    params = {}
    if location_id:
        params["locationId"] = location_id
    elif client.location_id:
        params["locationId"] = client.location_id

    response = client.get("/objects/", params=params)
    response.raise_for_status()
    return response.json()

def get_schema(client: GHLClient, key: str, location_id: Optional[str] = None) -> Dict[str, Any]:
    params = {}
    if location_id:
        params["locationId"] = location_id
    elif client.location_id:
        params["locationId"] = client.location_id

    response = client.get(f"/objects/{key}", params=params)
    response.raise_for_status()
    return response.json()

def list_records(client: GHLClient, schema_key: str, limit: int = 20, query: Optional[str] = None, location_id: Optional[str] = None) -> Dict[str, Any]:
    data = {
        "pageLimit": limit,
        "page": 1, # Default to page 1 for now
    }
    if query:
        data["query"] = query

    if location_id:
        data["locationId"] = location_id
    elif client.location_id:
        data["locationId"] = client.location_id

    response = client.post(f"/objects/{schema_key}/records/search", json=data)
    response.raise_for_status()
    return response.json()

def get_record(client: GHLClient, schema_key: str, record_id: str) -> Dict[str, Any]:
    response = client.get(f"/objects/{schema_key}/records/{record_id}")
    response.raise_for_status()
    return response.json()

def create_record(client: GHLClient, schema_key: str, data: Dict[str, Any]) -> Dict[str, Any]:
    response = client.post(f"/objects/{schema_key}/records", json=data)
    response.raise_for_status()
    return response.json()

def update_record(client: GHLClient, schema_key: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    response = client.put(f"/objects/{schema_key}/records/{record_id}", json=data)
    response.raise_for_status()
    return response.json()

def delete_record(client: GHLClient, schema_key: str, record_id: str) -> Dict[str, Any]:
    response = client.delete(f"/objects/{schema_key}/records/{record_id}")
    response.raise_for_status()
    return response.json()
