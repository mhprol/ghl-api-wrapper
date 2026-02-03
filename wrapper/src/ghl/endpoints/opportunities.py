from typing import Optional, Dict, Any
from ..client import GHLClient

def list_opportunities(client: GHLClient, limit: int = 20, query: Optional[str] = None, pipeline_id: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
    params = {"limit": limit}
    if query:
        params["q"] = query
    if pipeline_id:
        params["pipeline_id"] = pipeline_id
    if status:
        params["status"] = status

    if client.location_id:
        params["location_id"] = client.location_id

    response = client.get("/opportunities/search", params=params)
    response.raise_for_status()
    return response.json()

def get_opportunity(client: GHLClient, opportunity_id: str) -> Dict[str, Any]:
    response = client.get(f"/opportunities/{opportunity_id}")
    response.raise_for_status()
    return response.json()

def create_opportunity(client: GHLClient, data: Dict[str, Any]) -> Dict[str, Any]:
    response = client.post("/opportunities/", json=data)
    response.raise_for_status()
    return response.json()

def update_opportunity(client: GHLClient, opportunity_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    response = client.put(f"/opportunities/{opportunity_id}", json=data)
    response.raise_for_status()
    return response.json()

def delete_opportunity(client: GHLClient, opportunity_id: str) -> Dict[str, Any]:
    response = client.delete(f"/opportunities/{opportunity_id}")
    response.raise_for_status()
    return response.json()

def list_pipelines(client: GHLClient) -> Dict[str, Any]:
    params = {}
    if client.location_id:
        params["locationId"] = client.location_id

    response = client.get("/opportunities/pipelines", params=params)
    response.raise_for_status()
    return response.json()
