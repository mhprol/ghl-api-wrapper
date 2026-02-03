import httpx
from typing import Optional, Dict, Any

class GHLClient:
    BASE_URL = "https://services.leadconnectorhq.com"

    def __init__(self, api_key: str, location_id: Optional[str] = None):
        self.api_key = api_key
        self.location_id = location_id

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Version": "2021-07-28"
        }

        self.client = httpx.Client(
            base_url=self.BASE_URL,
            headers=headers,
            timeout=30.0
        )

    def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return self.client.get(url, params=params)

    def post(self, url: str, json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return self.client.post(url, json=json, params=params)

    def put(self, url: str, json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return self.client.put(url, json=json, params=params)

    def delete(self, url: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return self.client.delete(url, params=params)
