from typing import Optional, Dict, Any
from ..client import GHLClient

def list_calendars(client: GHLClient, location_id: Optional[str] = None, group_id: Optional[str] = None) -> Dict[str, Any]:
    params = {}
    if location_id:
        params["locationId"] = location_id
    elif client.location_id:
        params["locationId"] = client.location_id
    if group_id:
        params["groupId"] = group_id

    response = client.get("/calendars/", params=params)
    response.raise_for_status()
    return response.json()

def get_calendar(client: GHLClient, calendar_id: str) -> Dict[str, Any]:
    response = client.get(f"/calendars/{calendar_id}")
    response.raise_for_status()
    return response.json()

def create_calendar(client: GHLClient, data: Dict[str, Any]) -> Dict[str, Any]:
    response = client.post("/calendars/", json=data)
    response.raise_for_status()
    return response.json()

def update_calendar(client: GHLClient, calendar_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    response = client.put(f"/calendars/{calendar_id}", json=data)
    response.raise_for_status()
    return response.json()

def delete_calendar(client: GHLClient, calendar_id: str) -> Dict[str, Any]:
    response = client.delete(f"/calendars/{calendar_id}")
    response.raise_for_status()
    return response.json()

def list_events(client: GHLClient, start_time: str, end_time: str, calendar_id: Optional[str] = None, group_id: Optional[str] = None, user_id: Optional[str] = None) -> Dict[str, Any]:
    params = {
        "startTime": start_time,
        "endTime": end_time
    }
    if client.location_id:
        params["locationId"] = client.location_id

    if calendar_id:
        params["calendarId"] = calendar_id
    if group_id:
        params["groupId"] = group_id
    if user_id:
        params["userId"] = user_id

    response = client.get("/calendars/events", params=params)
    response.raise_for_status()
    return response.json()

def get_event(client: GHLClient, event_id: str) -> Dict[str, Any]:
    response = client.get(f"/calendars/events/appointments/{event_id}")
    response.raise_for_status()
    return response.json()

def create_event(client: GHLClient, data: Dict[str, Any]) -> Dict[str, Any]:
    response = client.post("/calendars/events/appointments", json=data)
    response.raise_for_status()
    return response.json()

def update_event(client: GHLClient, event_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
    response = client.put(f"/calendars/events/appointments/{event_id}", json=data)
    response.raise_for_status()
    return response.json()

def delete_event(client: GHLClient, event_id: str) -> Dict[str, Any]:
    response = client.delete(f"/calendars/events/{event_id}")
    response.raise_for_status()
    return response.json()
