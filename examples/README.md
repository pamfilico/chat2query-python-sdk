# Chat2Query SDK Examples

This directory contains example scripts demonstrating various features of the Chat2Query Python SDK.

## Prerequisites

Before running these examples:

1. Install the SDK:
   ```bash
   pip install chat2query-python-sdk
   ```

2. Get your API key from the Chat2Query dashboard

3. Update the `api_key` and `base_url` in each example script

## Examples

### 1. Basic Usage (`basic_usage.py`)

Demonstrates the fundamental workflow:
- Initialize the SDK client
- List available databases
- Create a chat with a natural language question
- Execute the generated SQL query
- View results

```bash
python examples/basic_usage.py
```

### 2. Database Management (`create_database.py`)

Shows how to manage database connections:
- Create a new database connection
- Update database information
- Retrieve database details
- List all databases
- Delete databases

```bash
python examples/create_database.py
```

### 3. Multi-turn Conversation (`conversation.py`)

Demonstrates conversational interactions:
- Start a conversation with an initial question
- Ask follow-up questions
- View message history
- Execute queries throughout the conversation

```bash
python examples/conversation.py
```

## Configuration

Each example requires configuration:

```python
client = Chat2QueryClient(
    api_key="your-api-key-here",    # Replace with your API key
    base_url="http://localhost:5000" # Replace with your API URL
)
```

For production use:
```python
client = Chat2QueryClient(
    api_key="your-api-key-here",
    base_url="https://api.chat2query.com"
)
```

## Error Handling

All examples include proper error handling:

```python
from chat2query.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError
)

try:
    # Your code here
except AuthenticationError:
    print("Invalid API key")
except NotFoundError:
    print("Resource not found")
except APIError as e:
    print(f"API error: {e}")
```

## Next Steps

After running these examples, check out the main README for:
- Complete API reference
- Advanced usage patterns
- Best practices
