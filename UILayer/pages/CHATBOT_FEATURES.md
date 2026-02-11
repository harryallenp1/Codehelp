# Chatbot Chat History Feature

## Overview
The Educational Chat Assistant now includes the ability to save and manage chat conversations during a session.

## Features Implemented

### 1. Session Chat History
- **Global Dictionary**: `chat_history` - stores all messages as a list of objects
- **Persistent Storage**: Uses `dcc.Store` component to maintain chat history across callbacks
- Each message object contains:
  - `timestamp`: When the message was sent (YYYY-MM-DD HH:MM:SS format)
  - `user_input`: The question asked by the user
  - `assistant_response`: The answer provided by the chatbot

### 2. Save Chat Functionality
- **Button**: "Save Chat" (green button)
- **Action**: Saves the current chat session as a JSON file
- **Location**: `UILayer/pages/saved_chats/`
- **Filename Format**: `chat_history_YYYYMMDD_HHMMSS.json`
- **Feedback**: Shows success/warning alert after save attempt

### 3. Clear Chat Functionality
- **Button**: "Clear Chat" (yellow/warning button)
- **Action**: Clears the current conversation and resets the chat window
- **Effect**: Clears both global `chat_history` and the stored state

### 4. Enhanced Display
- Shows timestamp for each message
- Formats messages with markdown for better readability
- Separates messages with horizontal rules
- Auto-scrolls to show latest messages

## Code Structure

### Callbacks

#### 1. `update_chat(n_clicks, user_input, stored_history)`
- **Triggers**: When "Send" button is clicked
- **Inputs**: Button clicks, user input text, stored chat history
- **Outputs**: Updated chat display, cleared input field, updated stored history
- **Process**:
  1. Gets response from `Send_Query()`
  2. Creates message object with timestamp
  3. Appends to global `chat_history`
  4. Updates stored history
  5. Builds formatted display text
  6. Clears input field

#### 2. `save_chat_to_json(n_clicks, stored_history)`
- **Triggers**: When "Save Chat" button is clicked
- **Inputs**: Button clicks, stored chat history
- **Outputs**: Status message (success/warning alert)
- **Process**:
  1. Validates chat history exists
  2. Creates `saved_chats` directory if needed
  3. Generates timestamped filename
  4. Saves chat as formatted JSON
  5. Shows success message

#### 3. `clear_chat(n_clicks)`
- **Triggers**: When "Clear Chat" button is clicked
- **Inputs**: Button clicks
- **Outputs**: Reset chat display, cleared stored history
- **Process**:
  1. Clears global `chat_history`
  2. Resets display to initial state
  3. Clears stored history

## Usage Example

### For Students:
1. Ask questions in the chat interface
2. Review the conversation as it builds
3. Click "Save Chat" to save the conversation for later reference
4. Click "Clear Chat" to start a new conversation

### Saved JSON Structure:
```json
[
    {
        "timestamp": "2026-02-10 14:30:45",
        "user_input": "What careers are available?",
        "assistant_response": "There are many careers..."
    }
]
```

## Technical Details

### Dependencies Added:
- `json` - for JSON file operations
- `datetime` - for timestamps
- `os` - for directory operations

### State Management:
- **Global Variable**: `chat_history = []` - maintains session state
- **dcc.Store**: `chat-history-store` - persists data across callbacks
- **Dual Storage**: Ensures data consistency and callback communication

### File System:
- Directory: `UILayer/pages/saved_chats/`
- Auto-created on first save
- Includes `.gitignore` to prevent committing user chats
- Includes `README.md` for documentation

## Future Enhancements (Optional)

1. **Load Previous Chats**: Add ability to load and continue previous conversations
2. **Export Options**: Add PDF or text export formats
3. **Search History**: Search through saved conversations
4. **Session Management**: Multiple concurrent chat sessions
5. **User Authentication**: Associate chats with specific users
6. **Chat Sharing**: Share conversations with advisors or peers

## Testing

To test the implementation:
1. Start the Dash application
2. Navigate to the chatbot page
3. Send several messages
4. Click "Save Chat" - verify JSON file is created
5. Click "Clear Chat" - verify conversation resets
6. Check `UILayer/pages/saved_chats/` for saved files
