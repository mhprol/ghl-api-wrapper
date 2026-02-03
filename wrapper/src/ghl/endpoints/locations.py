from typing import Optional, Dict, Any
from ..client import GHLClient

def list_locations(client: GHLClient, limit: int = 10, skip: int = 0, email: Optional[str] = None, company_id: Optional[str] = None) -> Dict[str, Any]:
    params = {
        "limit": limit,
        "skip": skip
    }
    if email:
        params["email"] = email
    if company_id:
        params["companyId"] = company_id

    response = client.get("/locations/search", params=params)
    response.raise_for_status()
    return response.json()

def get_location(client: GHLClient, location_id: str) -> Dict[str, Any]:
    response = client.get(f"/locations/{location_id}")
    response.raise_for_status()
    return response.json()

def create_location(client: GHLClient, data: Dict[str, Any]) -> Dict[str, Any]:
    response = client.post("/locations/", json=data)
    response.raise_for_status()
    return response.json()

def update_location(client: GHLClient, location_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    response = client.put(f"/locations/{location_id}", json=data)
    response.raise_for_status()
    return response.json()

def delete_location(client: GHLClient, location_id: str, delete_twilio_account: bool = False) -> Dict[str, Any]:
    params = {"deleteTwilioAccount": delete_twilio_account}
    response = client.delete(f"/locations/{location_id}", params=params)
    response.raise_for_status()
    return response.json()
