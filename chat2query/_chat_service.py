"""Internal chat service used by Chat2QueryService."""

from __future__ import annotations

from typing import Any, Dict, Optional

from chat2query.exceptions import APIError


class _ChatService:
    """Encapsulates chat CRUD operations for Chat2QueryService."""

    def __init__(self, sdk_service: "Chat2QueryService"):
        self._service = sdk_service

    def list_for_database(self, database_id: int) -> Any:
        """Fetch all chats for a specific database."""
        response = self._service._request(
            "GET", f"/api/v1/chat2/db/{database_id}"
        )
        data = response.get("data")
        if data is None:
            raise APIError("Chat list response did not include data")
        return data

    def get(self, chat_id: int) -> Dict[str, Any]:
        """Retrieve chat metadata by id."""
        response = self._service._request("GET", f"/api/v1/chat2/{chat_id}")
        data = response.get("data")
        if data is None:
            raise APIError("Chat response did not include data")
        if not isinstance(data, dict):
            raise APIError("Chat response was not an object")
        return data

    def create(
        self,
        *,
        database_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a new chat for the provided database."""
        payload: Dict[str, Any] = {
            "database_id": database_id,
            "name": name,
            "description": description,
        }
        response = self._service._request("POST", "/api/v1/chat2", data=payload)
        data = response.get("data")
        if data is None:
            raise APIError("Create chat response did not include data")
        return data

    def update(
        self,
        chat_id: int,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Update chat name/description."""
        payload = {
            key: value
            for key, value in {
                "name": name,
                "description": description,
            }.items()
            if value is not None
        }
        if not payload:
            raise APIError("At least one field must be provided to update a chat")

        response = self._service._request(
            "PUT", f"/api/v1/chat2/{chat_id}", data=payload
        )
        data = response.get("data")
        if data is None:
            raise APIError("Update chat response did not include data")
        return data

    def delete(self, chat_id: int) -> None:
        """Deleting chats is restricted to the web application."""
        raise APIError("Deleting chats is only available in the web application.")
