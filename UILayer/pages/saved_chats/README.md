# Saved Chat Conversations

This directory stores chat conversations that users choose to save from the Educational Chat Assistant.

## File Format

Each saved chat is stored as a JSON file with the following structure:

```json
[
    {
        "timestamp": "2026-02-10 14:30:45",
        "user_input": "What careers are available in computer science?",
        "assistant_response": "There are many exciting careers in computer science..."
    },
    {
        "timestamp": "2026-02-10 14:31:20",
        "user_input": "What skills do I need?",
        "assistant_response": "Key skills include programming, problem-solving..."
    }
]
```

## Filename Convention

Files are named using the pattern: `chat_history_YYYYMMDD_HHMMSS.json`

Example: `chat_history_20260210_143045.json`

## Usage

- Users can save their chat conversations by clicking the "Save Chat" button in the chatbot interface
- Saved chats can be loaded and reviewed later
- The directory is automatically created when the first chat is saved
