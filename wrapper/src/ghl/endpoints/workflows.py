from typing import Optional, Dict, Any
from ..client import GHLClient

def list_workflows(client: GHLClient, location_id: Optional[str] = None) -> Dict[str, Any]:
    params = {}
    if location_id:
        params["locationId"] = location_id
    elif client.location_id:
        params["locationId"] = client.location_id

    response = client.get("/workflows/", params=params)
    response.raise_for_status()
    return response.json()
