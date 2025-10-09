"""Chat2Query SDK quickstart script.

Run this after starting the Chat2Query backend and providing a reachable
PostgreSQL database URI. The script walks through:

1. Initializing the service with an application API key
2. Creating (or reusing) a database record
3. Opening a chat for that database
4. Asking a natural-language question and printing the generated SQL
"""

from __future__ import annotations

from chat2query import Chat2QueryService
from chat2query.exceptions import APIError


def main() -> None:
    # Replace these with your own values.
    api_key = "c2q-REPLACE-ME"
    base_url = "http://localhost:5000"  # or https://chat2query.com
    database_uri = "postgresql://user:pass@localhost:5432/yourdb"

    service = Chat2QueryService(api_key=api_key, base_url=base_url)

    try:
        database = service.databases.create(
            name="SDK Demo Database",
            database_uri=database_uri,
            description="Created via Chat2Query Python SDK quickstart",
        )
    except APIError as exc:
        # If the database already exists, reuse it by name.
        if "already exists" not in str(exc).lower():
            raise
        existing = [
            db for db in service.databases.list() if db["name"] == "SDK Demo Database"
        ]
        if not existing:
            raise
        database = existing[0]

    chat = service.chats.create(
        database_id=database["id"],
        name="SDK Demo Conversation",
        description="Testing Chat2Query via SDK",
    )

    history = service.messages.ask(
        chat_id=chat["id"], prompt="Show the top 10 customers by lifetime spend"
    )

    latest = history[0]
    print("Generated SQL:\n", latest["response"])


if __name__ == "__main__":
    main()
