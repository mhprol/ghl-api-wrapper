import httpx
from typing import Optional, Dict, Any

class GHLClient:
    BASE_URL = "https://services.leadconnectorhq.com"

    def __init__(self, api_key: str, location_id: Optional[str] = None, client: Optional[httpx.Client] = None,
                 client_id: Optional[str] = None, client_secret: Optional[str] = None, refresh_token: Optional[str] = None):
        self.api_key = api_key
        self.location_id = location_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Version": "2021-07-28"
        }

        self.client = client or httpx.Client(
            base_url=self.BASE_URL,
            headers=headers,
            timeout=30.0
        )

    def refresh_access_token(self) -> Dict[str, Any]:
        """Refreshes the access token using the refresh token."""
        if not (self.client_id and self.client_secret and self.refresh_token):
            raise ValueError("client_id, client_secret, and refresh_token are required for token refresh")

        url = f"{self.BASE_URL}/oauth/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "user_type": "Location"
        }

        # Use a separate client for the refresh call to avoid headers from the main client
        with httpx.Client() as token_client:
            response = token_client.post(url, data=data)

        # Handle response manually here as we don't want to trigger recursion via _handle_response
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            # We can try to enrich the error message here too
            raise e

        token_data = response.json()
        self.api_key = token_data["access_token"]
        if "refresh_token" in token_data:
            self.refresh_token = token_data["refresh_token"]

        # Update the main client headers
        self.client.headers["Authorization"] = f"Bearer {self.api_key}"

        return token_data

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

    def _make_request(self, method: str, url: str, **kwargs) -> httpx.Response:
        try:
            response = getattr(self.client, method)(url, **kwargs)
            return self._handle_response(response)
        except httpx.HTTPStatusError as e:
            # Check for 401 and if we have refresh capabilities
            if e.response.status_code == 401 and self.refresh_token:
                try:
                    self.refresh_access_token()
                    # Retry the original request with new token
                    response = getattr(self.client, method)(url, **kwargs)
                    return self._handle_response(response)
                except Exception:
                    # If refresh fails, or retry fails, raise the original error (or the new one).
                    # Raising the original error might be less confusing if refresh failed silently,
                    # but if refresh failed explicitly, we should probably know.
                    # Let's raise the new error if refresh failed.
                    raise
            raise e

    def get(self, url: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return self._make_request("get", url, params=params)

    def post(self, url: str, json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return self._make_request("post", url, json=json, params=params)

    def put(self, url: str, json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return self._make_request("put", url, json=json, params=params)

    def delete(self, url: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        return self._make_request("delete", url, params=params)
