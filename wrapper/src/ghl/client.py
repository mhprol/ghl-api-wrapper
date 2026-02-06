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

    def _handle_response(self, response: httpx.Response) -> httpx.Response:
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            message = str(e)
            try:
                # Try to extract detailed error message from response body
                data = response.json()
                if isinstance(data, dict):
                    if "message" in data:
                        message += f" - {data['message']}"
                    elif "error" in data:
                        message += f" - {data['error']}"
                    elif "msg" in data:
                        message += f" - {data['msg']}"
                    else:
                        message += f" - {data}"
                else:
                    message += f" - {data}"
            except Exception:
                # If json decoding fails or other error, just use original message or check text
                if response.content:
                    # Limit content length to avoid huge log
                    content_str = response.text[:200]
                    if content_str:
                        message += f" - {content_str}"

            raise httpx.HTTPStatusError(message, request=e.request, response=e.response) from e

        return response

    def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        response = self.client.get(url, params=params)
        return self._handle_response(response)

    def post(self, url: str, json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        response = self.client.post(url, json=json, params=params)
        return self._handle_response(response)

    def put(self, url: str, json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        response = self.client.put(url, json=json, params=params)
        return self._handle_response(response)

    def delete(self, url: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        response = self.client.delete(url, params=params)
        return self._handle_response(response)
