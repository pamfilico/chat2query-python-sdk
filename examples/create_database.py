"""
Example: Creating and managing database connections

This example demonstrates:
1. Creating a new database connection
2. Updating database information
3. Getting database details
4. Listing all databases
"""

from chat2query import Chat2QueryClient
from chat2query.exceptions import APIError


def main():
    # Initialize the client
    client = Chat2QueryClient(
        api_key="your-api-key-here",
        base_url="http://localhost:5000"
    )

    try:
        print("=" * 60)
        print("Database Management Example")
        print("=" * 60)

        # Create a new database connection
        print("\n1. Creating a new database connection...")
        new_database = client.databases.create(
            name="Example PostgreSQL DB",
            database_uri="postgresql://user:password@localhost:5432/example_db",
            description="Example database for testing"
        )

        database_id = new_database["id"]
        print(f"   ✓ Database created with ID: {database_id}")
        print(f"   Name: {new_database['name']}")
        print(f"   Description: {new_database['description']}")

        # Get database details
        print("\n2. Getting database details...")
        database = client.databases.get(database_id=database_id)
        print(f"   ✓ Retrieved database: {database['name']}")

        # Update database
        print("\n3. Updating database information...")
        updated_database = client.databases.update(
            database_id=database_id,
            name="Updated Example DB",
            description="Updated description"
        )
        print(f"   ✓ Database updated")
        print(f"   New name: {updated_database['name']}")
        print(f"   New description: {updated_database['description']}")

        # List all databases
        print("\n4. Listing all databases...")
        all_databases = client.databases.list()
        print(f"   ✓ Found {len(all_databases)} database(s):")
        for db in all_databases:
            print(f"     - {db['name']} (ID: {db['id']})")

        # Optional: Delete the database
        print("\n5. Cleanup (delete example database)...")
        response = input("   Delete the example database? (y/n): ")
        if response.lower() == 'y':
            client.databases.delete(database_id=database_id)
            print("   ✓ Database deleted")

        print("\n" + "=" * 60)
        print("Example completed successfully!")
        print("=" * 60)

    except APIError as e:
        print(f"\n❌ API error: {e}")
        if hasattr(e, 'status_code'):
            print(f"   Status code: {e.status_code}")


if __name__ == "__main__":
    main()
