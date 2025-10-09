"""Service helper for Chat2Query application API key integrations."""

from __future__ import annotations

from typing import Any, Dict, Optional

import requests

from chat2query.exceptions import APIError, AuthenticationError
from chat2query._database_service import _DatabaseService
from chat2query._chat_service import _ChatService
from chat2query._message_service import _MessageService


class Chat2QueryService:
    """
    Lightweight service for integrating with the Chat2Query backend via application API keys.

    The service pings the backend on initialization to verify the key and cache the user id.
    """

    DEFAULT_BASE_URL = "https://chat2query.com"

    def __init__(self, api_key: str, base_url: Optional[str] = None):
        self.api_key = api_key
        resolved_base_url = base_url or self.DEFAULT_BASE_URL
        self.base_url = resolved_base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "APPLICATION-API-KEY": api_key,
                "APPLICATION_API_KEY": api_key,
                "Content-Type": "application/json",
            }
        )
        self.user_id: Optional[int] = None
        self.databases = _DatabaseService(self)
        self.chats = _ChatService(self)
        self.messages = _MessageService(self)

        # Verify connectivity immediately so failures surface early.
        self._verify_connection()

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Perform an HTTP request with application API key authentication."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
            )
        except requests.exceptions.RequestException as exc:
            raise APIError(f"Request failed: {exc}") from exc

        if response.status_code == 401:
            raise AuthenticationError("Invalid application API key")

        if response.status_code >= 400:
            message: str
            try:
                payload = response.json()
                message = payload.get("ui_message") or payload.get("message", "Unknown error")
            except ValueError:
                message = response.text or "Unknown error"
            raise APIError(message, status_code=response.status_code)

        try:
            return response.json()
        except ValueError as exc:
            raise APIError(f"Invalid JSON response: {exc}") from exc

    def _verify_connection(self) -> None:
        """Ping the backend to confirm the key is valid and cache the user id."""
        user_id = self.ping()
        self.user_id = user_id

    def ping(self) -> int:
        """
        Hit the SDK ping endpoint and return the authenticated user's id.

        Returns:
            int: The user id associated with the API key.

        Raises:
            APIError: If the response does not contain a user id.
        """
        response = self._request("GET", "/api/v1/sdk/ping")
        data = response.get("data") or {}
        user_id = data.get("user_id")
        if user_id is None:
            raise APIError("SDK ping response did not include a user id")
        self.user_id = user_id
        return user_id
