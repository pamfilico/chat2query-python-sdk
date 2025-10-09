"""Chat2Query SDK Client"""

from typing import Any, Dict, List, Optional

import requests

from chat2query.exceptions import APIError, AuthenticationError, NotFoundError


class Chat2QueryClient:
    """
    Client for interacting with the Chat2Query API.

    Args:
        api_key: Your Chat2Query API key
        base_url: Base URL for the API (default: http://localhost:5000)
    """

    def __init__(self, api_key: str, base_url: str = "http://localhost:5000"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "LIBRARY-TOKEN": api_key,
                "Content-Type": "application/json",
            }
        )

        # Initialize resource managers
        self.databases = DatabaseResource(self)
        self.chats = ChatResource(self)
        self.messages = MessageResource(self)
        self.executor = ExecutorResource(self)

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (without base URL)
            data: Request body data
            params: Query parameters

        Returns:
            Response data

        Raises:
            AuthenticationError: If authentication fails
            APIError: If API returns an error
            NotFoundError: If resource is not found
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
            )

            # Check for authentication errors
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key")

            # Check for not found errors
            if response.status_code == 404:
                raise NotFoundError("Resource not found", status_code=404)

            # Check for other errors
            if response.status_code >= 400:
                error_message = response.json().get("message", "Unknown error")
                raise APIError(error_message, status_code=response.status_code)

            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise APIError(f"Request failed: {str(e)}")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request"""
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request"""
        return self._request("POST", endpoint, data=data)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PUT request"""
        return self._request("PUT", endpoint, data=data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request"""
        return self._request("DELETE", endpoint)


class DatabaseResource:
    """Manage database connections"""

    def __init__(self, client: Chat2QueryClient):
        self.client = client

    def list(self) -> List[Dict[str, Any]]:
        """
        List all databases.

        Returns:
            List of database objects
        """
        response = self.client.get("/api/v1/database")
        return response.get("data", [])

    def get(self, database_id: int) -> Dict[str, Any]:
        """
        Get a specific database.

        Args:
            database_id: Database ID

        Returns:
            Database object
        """
        response = self.client.get(f"/api/v1/database/{database_id}")
        return response.get("data", {})

    def create(
        self,
        name: str,
        database_uri: str,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new database connection.

        Args:
            name: Database name
            database_uri: Database connection URI
            description: Optional description

        Returns:
            Created database object
        """
        data = {
            "name": name,
            "database_uri": database_uri,
            "description": description,
        }
        response = self.client.post("/api/v1/database", data=data)
        return response.get("data", {})

    def update(
        self,
        database_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update a database.

        Args:
            database_id: Database ID
            name: New name
            description: New description

        Returns:
            Updated database object
        """
        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description

        response = self.client.put(f"/api/v1/database/{database_id}", data=data)
        return response.get("data", {})

    def delete(self, database_id: int) -> Dict[str, Any]:
        """
        Delete a database.

        Args:
            database_id: Database ID

        Returns:
            Deletion confirmation
        """
        return self.client.delete(f"/api/v1/database/{database_id}")


class ChatResource:
    """Manage chat sessions"""

    def __init__(self, client: Chat2QueryClient):
        self.client = client

    def list(self, database_id: int) -> List[Dict[str, Any]]:
        """
        List all chats for a database.

        Args:
            database_id: Database ID

        Returns:
            List of chat objects
        """
        response = self.client.get(f"/api/v1/database/{database_id}/chat")
        return response.get("data", [])

    def get(self, database_id: int, chat_id: int) -> Dict[str, Any]:
        """
        Get a specific chat.

        Args:
            database_id: Database ID
            chat_id: Chat ID

        Returns:
            Chat object
        """
        response = self.client.get(f"/api/v1/database/{database_id}/chat/{chat_id}")
        return response.get("data", {})

    def create(self, database_id: int, question: str) -> Dict[str, Any]:
        """
        Create a new chat session and ask a question.

        Args:
            database_id: Database ID
            question: Natural language question

        Returns:
            Created chat object with generated SQL query
        """
        data = {"question": question}
        response = self.client.post(f"/api/v1/database/{database_id}/chat", data=data)
        return response.get("data", {})

    def delete(self, database_id: int, chat_id: int) -> Dict[str, Any]:
        """
        Delete a chat.

        Args:
            database_id: Database ID
            chat_id: Chat ID

        Returns:
            Deletion confirmation
        """
        return self.client.delete(f"/api/v1/database/{database_id}/chat/{chat_id}")


class MessageResource:
    """Manage chat messages"""

    def __init__(self, client: Chat2QueryClient):
        self.client = client

    def list(self, database_id: int, chat_id: int) -> List[Dict[str, Any]]:
        """
        List all messages in a chat.

        Args:
            database_id: Database ID
            chat_id: Chat ID

        Returns:
            List of message objects
        """
        response = self.client.get(f"/api/v1/database/{database_id}/chat/{chat_id}/message")
        return response.get("data", [])

    def create(self, database_id: int, chat_id: int, question: str) -> Dict[str, Any]:
        """
        Send a new message in a chat.

        Args:
            database_id: Database ID
            chat_id: Chat ID
            question: Natural language question

        Returns:
            Created message object with generated SQL query
        """
        data = {"question": question}
        response = self.client.post(
            f"/api/v1/database/{database_id}/chat/{chat_id}/message",
            data=data,
        )
        return response.get("data", {})


class ExecutorResource:
    """Execute SQL queries"""

    def __init__(self, client: Chat2QueryClient):
        self.client = client

    def execute(self, database_id: int, chat_id: int) -> Dict[str, Any]:
        """
        Execute the SQL query for a chat.

        Args:
            database_id: Database ID
            chat_id: Chat ID

        Returns:
            Query results with data and column names
        """
        data = {
            "database_id": database_id,
            "chat_id": chat_id,
        }
        response = self.client.post("/api/v1/executor", data=data)
        return response.get("data", {})


def hello_world() -> str:
    """
    Returns a hello world message.

    Returns:
        str: Hello world message
    """
    return "Hello from Chat2Query Python SDK!"
