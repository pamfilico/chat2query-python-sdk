"""Tests for Chat2Query SDK modules."""

import pytest
import requests

from chat2query import Chat2QueryClient, Chat2QueryService, hello_world
from chat2query.exceptions import APIError

TEST_APPLICATION_API_KEY = "c2q-Auh8LOhT9LHBwaCQV95h75LXS7GKpWPlPU5B5Sqymjw"
LOCAL_BASE_URL = "http://localhost:5000"


@pytest.fixture(scope="module")
def ensure_local_backend():
    """Ensure the local backend is reachable; skip tests if not."""
    headers = {
        "APPLICATION-API-KEY": TEST_APPLICATION_API_KEY,
        "APPLICATION_API_KEY": TEST_APPLICATION_API_KEY,
    }
    try:
        response = requests.get(f"{LOCAL_BASE_URL}/api/v1/sdk/ping", headers=headers, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        pytest.skip(f"Local backend not reachable: {exc}")

    payload = response.json()
    data = payload.get("data") if isinstance(payload, dict) else None
    user_id = data.get("user_id") if isinstance(data, dict) else None
    if user_id is None:
        pytest.skip("Local backend ping did not return a user_id")
    return user_id


@pytest.fixture
def live_service(ensure_local_backend):
    """Provide an initialized service hitting the local backend."""
    return Chat2QueryService(api_key=TEST_APPLICATION_API_KEY, base_url=LOCAL_BASE_URL)


def test_hello_world():
    """Test hello_world function"""
    result = hello_world()
    assert result == "Hello from Chat2Query Python SDK!"
    assert isinstance(result, str)


def test_client_initialization():
    """Test client initialization"""
    client = Chat2QueryClient(
        api_key="test-key",
        base_url=LOCAL_BASE_URL
    )

    assert client.api_key == "test-key"
    assert client.base_url == LOCAL_BASE_URL
    assert client.session.headers["LIBRARY-TOKEN"] == "test-key"
    assert client.session.headers["Content-Type"] == "application/json"


def test_client_has_resources():
    """Test that client has all resource managers"""
    client = Chat2QueryClient(api_key="test-key")

    assert hasattr(client, "databases")
    assert hasattr(client, "chats")
    assert hasattr(client, "messages")
    assert hasattr(client, "executor")


def test_base_url_trailing_slash():
    """Test that trailing slash is removed from base URL"""
    client = Chat2QueryClient(
        api_key="test-key",
        base_url=f"{LOCAL_BASE_URL}/"
    )

    assert client.base_url == LOCAL_BASE_URL


def test_service_initialization_hits_local_backend(live_service, ensure_local_backend):
    """Service should ping local backend on init and cache user id"""
    assert isinstance(live_service.user_id, int)
    assert live_service.user_id == ensure_local_backend


def test_service_ping_returns_live_user_id(live_service, ensure_local_backend):
    """Service ping should return the live user id from local backend"""
    returned_user_id = live_service.ping()

    assert isinstance(returned_user_id, int)
    assert returned_user_id == ensure_local_backend
    assert live_service.user_id == ensure_local_backend


def test_service_list_databases_live(live_service):
    """List databases using live backend"""
    databases = live_service.databases.list()
    assert isinstance(databases, list)


def test_service_get_database_not_found(live_service):
    """Fetching an unknown database should raise APIError"""
    with pytest.raises(APIError):
        live_service.databases.get(database_id=0)


def test_service_create_database_requires_valid_uri(live_service):
    """Creating with an invalid URI should raise APIError from backend validation"""
    with pytest.raises(APIError):
        live_service.databases.create(
            name="SDK Test Database",
            database_uri="postgresql://invalid-host/testdb",
            description="Temporary test database",
        )


def test_service_update_database_requires_existing_record(live_service):
    """Updating a non-existent database should raise APIError"""
    with pytest.raises(APIError):
        live_service.databases.update(
            database_id=0,
            name="Updated Name",
        )


def test_service_delete_database_not_supported(live_service):
    """Deleting databases should inform users to use the web application"""
    with pytest.raises(APIError) as exc:
        live_service.databases.delete(database_id=0)
    assert "web application" in str(exc.value)


def test_service_default_base_url_constant():
    """Ensure default base URL points to production host."""
    assert Chat2QueryService.DEFAULT_BASE_URL == "https://chat2query.com"


def test_chat_service_delete_not_supported(live_service):
    """Deleting chats should inform users to use the web application"""
    with pytest.raises(APIError) as exc:
        live_service.chats.delete(chat_id=0)
    assert "web application" in str(exc.value)


def test_messages_list_requires_existing_chat(live_service):
    """Listing messages for unknown chat should raise APIError"""
    with pytest.raises(APIError):
        live_service.messages.list(chat_id=0)


def test_messages_ask_requires_valid_chat(live_service):
    """Asking a question for unknown chat should raise APIError"""
    with pytest.raises(APIError):
        live_service.messages.ask(chat_id=0, prompt="SELECT 1")


def test_messages_regenerate_requires_existing_message(live_service):
    """Regenerating unknown message should raise APIError"""
    with pytest.raises(APIError):
        live_service.messages.regenerate(message_id=0)


def test_messages_get_api_spec_requires_existing_message(live_service):
    """Fetching API spec for unknown message should raise APIError"""
    with pytest.raises(APIError):
        live_service.messages.get_api_spec(message_id=0)


def test_messages_delete_not_supported(live_service):
    """Deleting messages should be blocked in SDK"""
    with pytest.raises(APIError) as exc:
        live_service.messages.delete(message_id=0)
    assert "web application" in str(exc.value)
