"""Internal message service used by Chat2QueryService."""

from __future__ import annotations

from typing import Any, Dict, Optional

from chat2query.exceptions import APIError


class _MessageService:
    """Encapsulates message operations for Chat2QueryService."""

    def __init__(self, sdk_service: "Chat2QueryService"):
        self._service = sdk_service

    def list(self, chat_id: int) -> Any:
        """Return the message history for a chat (most recent first)."""
        response = self._service._request(
            "GET", f"/api/v1/message/chat/{chat_id}"
        )
        data = response.get("data")
        if data is None:
            raise APIError("Message list response did not include data")
        return data

    def ask(self, *, chat_id: int, prompt: str) -> Any:
        """Send a new prompt to the chat and return updated messages."""
        payload: Dict[str, Any] = {
            "chat_id": chat_id,
            "prompt": prompt,
        }
        response = self._service._request("POST", "/api/v1/message", data=payload)
        data = response.get("data")
        if data is None:
            raise APIError("Create message response did not include data")
        return data

    def regenerate(self, message_id: int) -> Any:
        """Regenerate an assistant response for an existing message."""
        response = self._service._request(
            "POST", f"/api/v1/message/{message_id}/regenerate"
        )
        data = response.get("data")
        if data is None:
            raise APIError("Regenerate message response did not include data")
        return data

    def get_api_spec(self, message_id: int) -> Dict[str, Any]:
        """Retrieve the API specification attached to a message."""
        response = self._service._request(
            "GET", f"/api/v1/message/{message_id}/apispec"
        )
        data = response.get("data")
        if data is None:
            raise APIError("API spec response did not include data")
        if not isinstance(data, dict):
            raise APIError("API spec response was not an object")
        return data

    def update_api_spec(
        self,
        message_id: int,
        *,
        spec: Dict[str, Any],
        active_api: bool,
    ) -> Dict[str, Any]:
        """Update the API spec linked to a message."""
        payload = {"spec": spec, "active_api": active_api}
        response = self._service._request(
            "PUT", f"/api/v1/message/{message_id}/apispec", data=payload
        )
        data = response.get("data")
        if data is None:
            raise APIError("Update API spec response did not include data")
        if not isinstance(data, dict):
            raise APIError("Update API spec response was not an object")
        return data

    def generate_description(self, message_id: int) -> Dict[str, Any]:
        """Generate API description/use-case text for a message."""
        response = self._service._request(
            "POST", f"/api/v1/message/{message_id}/generate-description"
        )
        data = response.get("data")
        if data is None:
            raise APIError("Generate message description response did not include data")
        if not isinstance(data, dict):
            raise APIError("Generate message description response was not an object")
        return data

    def get_api_usage(self, message_id: int) -> Dict[str, Any]:
        """Return API usage stats for a message."""
        response = self._service._request(
            "GET", f"/api/v1/message/{message_id}/api-usage"
        )
        data = response.get("data")
        if data is None:
            raise APIError("API usage response did not include data")
        if not isinstance(data, dict):
            raise APIError("API usage response was not an object")
        return data

    def flag(self, message_id: int) -> Any:
        """Flag a message for review."""
        response = self._service._request(
            "PUT", f"/api/v1/message/{message_id}/flag"
        )
        data = response.get("data")
        return data

    def delete(self, message_id: int) -> None:
        """Deleting messages is restricted to the web application."""
        raise APIError("Deleting messages is only available in the web application.")
