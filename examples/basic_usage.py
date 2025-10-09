"""
Basic usage example for Chat2Query Python SDK

This example demonstrates:
1. Initializing the client
2. Listing databases
3. Creating a chat with a question
4. Executing the generated query
5. Handling errors
"""

from chat2query import Chat2QueryClient
from chat2query.exceptions import APIError, AuthenticationError, NotFoundError


def main():
    # Initialize the client
    # Replace with your actual API key
    client = Chat2QueryClient(
        api_key="your-api-key-here",
        base_url="http://localhost:5000"  # Use your API base URL
    )

    try:
        print("=" * 60)
        print("Chat2Query Python SDK - Basic Usage Example")
        print("=" * 60)

        # List all databases
        print("\n1. Listing databases...")
        databases = client.databases.list()
        print(f"   Found {len(databases)} database(s)")

        if not databases:
            print("   No databases found. Please create one first.")
            return

        # Use the first database
        database = databases[0]
        database_id = database["id"]
        print(f"   Using database: {database['name']} (ID: {database_id})")

        # Create a chat with a question
        print("\n2. Creating a chat session...")
        question = "How many rows are in each table?"
        print(f"   Question: {question}")

        chat = client.chats.create(
            database_id=database_id,
            question=question
        )

        chat_id = chat["id"]
        generated_query = chat.get("query", "")
        print(f"   Chat created with ID: {chat_id}")
        print(f"   Generated SQL:\n   {generated_query}")

        # Execute the query
        print("\n3. Executing the query...")
        results = client.executor.execute(
            database_id=database_id,
            chat_id=chat_id
        )

        # Display results
        print("\n4. Query results:")
        column_names = results.get("column_names", [])
        data = results.get("data", [])

        if column_names:
            print(f"   Columns: {', '.join(column_names)}")

        if data:
            print(f"   Rows returned: {len(data)}")
            print("\n   First 5 rows:")
            for i, row in enumerate(data[:5], 1):
                print(f"   {i}. {row}")
        else:
            print("   No data returned")

        # List all chats for this database
        print("\n5. Listing all chats for this database...")
        all_chats = client.chats.list(database_id=database_id)
        print(f"   Total chats: {len(all_chats)}")

        print("\n" + "=" * 60)
        print("Example completed successfully!")
        print("=" * 60)

    except AuthenticationError:
        print("\n❌ Authentication failed. Please check your API key.")

    except NotFoundError as e:
        print(f"\n❌ Resource not found: {e}")

    except APIError as e:
        print(f"\n❌ API error: {e}")
        if hasattr(e, 'status_code'):
            print(f"   Status code: {e.status_code}")

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
