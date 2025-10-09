# Chat2Query Python SDK

<p align="center">
  <img src="whisper-to-robot-sql.svg" alt="Chat2Query - Natural Language to SQL" width="200"/>
</p>

Python SDK for interacting with the Chat2Query API. Convert natural language questions into SQL queries and execute them against your databases.

## Installation

```bash
pip install chat2query-python-sdk
```

Or using Poetry:

```bash
poetry add chat2query-python-sdk
```

## Quick Start

```python
from chat2query import Chat2QueryClient

# Initialize the client
client = Chat2QueryClient(
    api_key="your-api-key",
    base_url="https://api.chat2query.com"  # or http://localhost:5000 for local dev
)

# List your databases
databases = client.databases.list()
print(f"Found {len(databases)} databases")

# Create a chat and ask a question
database_id = databases[0]["id"]
chat = client.chats.create(
    database_id=database_id,
    question="How many users are in the system?"
)

print(f"Generated SQL: {chat['query']}")

# Execute the query
results = client.executor.execute(
    database_id=database_id,
    chat_id=chat["id"]
)

print(f"Results: {results['data']}")
```

## Features

- 🔐 **Authentication**: Secure API key authentication
- 🗄️ **Database Management**: List, create, update, and delete database connections
- 💬 **Chat Sessions**: Create conversations with your database
- 🤖 **Natural Language to SQL**: Convert questions to SQL queries using AI
- ⚡ **Query Execution**: Execute generated queries and get results
- 📝 **Message History**: Track conversation history within chats

## Usage

### Initialize the Client

```python
from chat2query import Chat2QueryClient

client = Chat2QueryClient(
    api_key="your-api-key",
    base_url="http://localhost:5000"
)
```

### Database Management

```python
# List all databases
databases = client.databases.list()

# Get a specific database
database = client.databases.get(database_id=1)

# Create a new database connection
new_db = client.databases.create(
    name="My PostgreSQL DB",
    database_uri="postgresql://user:password@localhost:5432/mydb",
    description="Production database"
)

# Update a database
updated_db = client.databases.update(
    database_id=1,
    name="Updated Name",
    description="Updated description"
)

# Delete a database
client.databases.delete(database_id=1)
```

### Chat Sessions

```python
# Create a new chat (asks a question)
chat = client.chats.create(
    database_id=1,
    question="What are the top 10 customers by revenue?"
)

# The response includes the generated SQL query
print(f"Generated SQL: {chat['query']}")

# List all chats for a database
chats = client.chats.list(database_id=1)

# Get a specific chat
chat = client.chats.get(database_id=1, chat_id=1)

# Delete a chat
client.chats.delete(database_id=1, chat_id=1)
```

### Messages

```python
# Continue a conversation by adding messages to a chat
message = client.messages.create(
    database_id=1,
    chat_id=1,
    question="Now show me the bottom 10"
)

# List all messages in a chat
messages = client.messages.list(database_id=1, chat_id=1)
```

### Query Execution

```python
# Execute the SQL query from a chat
results = client.executor.execute(
    database_id=1,
    chat_id=1
)

# Access the results
data = results["data"]  # List of rows
columns = results["column_names"]  # Column names
executed_at = results["executed_at"]  # Timestamp

# Print results as a table
for row in data:
    print(row)
```

## Complete Example

```python
from chat2query import Chat2QueryClient

# Initialize
client = Chat2QueryClient(
    api_key="your-api-key",
    base_url="http://localhost:5000"
)

# Create database connection
database = client.databases.create(
    name="Sales DB",
    database_uri="postgresql://user:pass@localhost:5432/sales",
    description="Sales analytics database"
)

# Ask a question
chat = client.chats.create(
    database_id=database["id"],
    question="What were the total sales last month?"
)

print(f"Generated SQL:\n{chat['query']}\n")

# Execute the query
results = client.executor.execute(
    database_id=database["id"],
    chat_id=chat["id"]
)

# Display results
print("Results:")
print(f"Columns: {results['column_names']}")
for row in results["data"]:
    print(row)

# Ask a follow-up question
follow_up = client.messages.create(
    database_id=database["id"],
    chat_id=chat["id"],
    question="How does that compare to the previous month?"
)

print(f"\nFollow-up SQL:\n{follow_up['query']}")
```

## Error Handling

```python
from chat2query import Chat2QueryClient
from chat2query.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    ValidationError
)

client = Chat2QueryClient(api_key="your-api-key")

try:
    database = client.databases.get(database_id=999)
except NotFoundError:
    print("Database not found")
except AuthenticationError:
    print("Invalid API key")
except APIError as e:
    print(f"API error: {e}")
    print(f"Status code: {e.status_code}")
```

## API Reference

### Client

- `Chat2QueryClient(api_key: str, base_url: str)` - Initialize the client

### Databases

- `client.databases.list()` - List all databases
- `client.databases.get(database_id: int)` - Get a database
- `client.databases.create(name: str, database_uri: str, description: str = None)` - Create database
- `client.databases.update(database_id: int, name: str = None, description: str = None)` - Update database
- `client.databases.delete(database_id: int)` - Delete database

### Chats

- `client.chats.list(database_id: int)` - List chats
- `client.chats.get(database_id: int, chat_id: int)` - Get a chat
- `client.chats.create(database_id: int, question: str)` - Create chat with question
- `client.chats.delete(database_id: int, chat_id: int)` - Delete chat

### Messages

- `client.messages.list(database_id: int, chat_id: int)` - List messages
- `client.messages.create(database_id: int, chat_id: int, question: str)` - Send message

### Executor

- `client.executor.execute(database_id: int, chat_id: int)` - Execute query

## Development

### Setup

```bash
# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=chat2query
```

### Building

```bash
# Build the package
poetry build

# Publish to PyPI
poetry publish
```

## Requirements

- Python 3.10 or higher
- requests library

## License

Proprietary
