"""
Example: Multi-turn conversation

This example demonstrates:
1. Starting a conversation with an initial question
2. Continuing the conversation with follow-up questions
3. Viewing message history
4. Executing queries from the conversation
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
        print("Multi-turn Conversation Example")
        print("=" * 60)

        # Get first database
        databases = client.databases.list()
        if not databases:
            print("No databases found. Please create one first.")
            return

        database = databases[0]
        database_id = database["id"]
        print(f"\nUsing database: {database['name']}")

        # Start a conversation
        print("\n1. Starting conversation...")
        initial_question = "What are the total sales for each product?"
        print(f"   You: {initial_question}")

        chat = client.chats.create(
            database_id=database_id,
            question=initial_question
        )

        chat_id = chat["id"]
        print(f"   SQL: {chat['query']}")

        # Execute first query
        print("\n2. Executing query...")
        results = client.executor.execute(
            database_id=database_id,
            chat_id=chat_id
        )
        print(f"   ✓ Query executed, returned {len(results.get('data', []))} rows")

        # Continue the conversation
        follow_ups = [
            "Now show me only the top 5 products",
            "What was the average order value?",
            "How many unique customers do we have?"
        ]

        for i, question in enumerate(follow_ups, 2):
            print(f"\n{i+1}. Follow-up question...")
            print(f"   You: {question}")

            message = client.messages.create(
                database_id=database_id,
                chat_id=chat_id,
                question=question
            )

            print(f"   SQL: {message['query']}")

            # Execute the query
            results = client.executor.execute(
                database_id=database_id,
                chat_id=chat_id
            )
            print(f"   ✓ Query executed, returned {len(results.get('data', []))} rows")

        # View conversation history
        print(f"\n{len(follow_ups)+3}. Viewing conversation history...")
        messages = client.messages.list(
            database_id=database_id,
            chat_id=chat_id
        )
        print(f"   Total messages in conversation: {len(messages)}")

        print("\n   Conversation summary:")
        for idx, msg in enumerate(messages, 1):
            question = msg.get('question', 'N/A')
            query = msg.get('query', 'N/A')
            print(f"\n   Message {idx}:")
            print(f"   Question: {question}")
            print(f"   SQL: {query[:80]}...")

        print("\n" + "=" * 60)
        print("Conversation completed successfully!")
        print("=" * 60)

    except APIError as e:
        print(f"\n❌ API error: {e}")
        if hasattr(e, 'status_code'):
            print(f"   Status code: {e.status_code}")


if __name__ == "__main__":
    main()
