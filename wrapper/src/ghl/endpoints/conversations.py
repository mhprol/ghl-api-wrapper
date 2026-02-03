from typing import Optional, Dict, Any
from ..client import GHLClient

def list_conversations(client: GHLClient, limit: int = 20, query: Optional[str] = None, status: Optional[str] = None, location_id: Optional[str] = None) -> Dict[str, Any]:
    params = {"limit": limit}
    if query:
        params["query"] = query
    if status:
        params["status"] = status
    if location_id:
        params["locationId"] = location_id
    elif client.location_id:
        params["locationId"] = client.location_id

    response = client.get("/conversations/search", params=params)
    response.raise_for_status()
    return response.json()

def get_conversation(client: GHLClient, conversation_id: str) -> Dict[str, Any]:
    response = client.get(f"/conversations/{conversation_id}")
    response.raise_for_status()
    return response.json()

def create_conversation(client: GHLClient, data: Dict[str, Any]) -> Dict[str, Any]:
    response = client.post("/conversations/", json=data)
    response.raise_for_status()
    return response.json()

def update_conversation(client: GHLClient, conversation_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    response = client.put(f"/conversations/{conversation_id}", json=data)
    response.raise_for_status()
    return response.json()

def delete_conversation(client: GHLClient, conversation_id: str) -> Dict[str, Any]:
    response = client.delete(f"/conversations/{conversation_id}")
    response.raise_for_status()
    return response.json()

def get_messages(client: GHLClient, conversation_id: str, limit: int = 20) -> Dict[str, Any]:
    params = {"limit": limit}
    response = client.get(f"/conversations/{conversation_id}/messages", params=params)
    response.raise_for_status()
    return response.json()
