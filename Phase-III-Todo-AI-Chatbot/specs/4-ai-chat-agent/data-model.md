# Data Model: AI Chat Agent & Integration

**Feature**: AI Chat Agent & Integration
**Date**: 2026-01-29

## Entity Definitions

### Conversation Entity
Represents a chat session between user and AI agent

**Fields**:
- `id`: UUID (Primary Key, auto-generated)
- `user_id`: UUID (Foreign Key to User, cascading delete)
- `title`: String (max 255 chars, summary of conversation topic, auto-generated from first message if not provided)
- `created_at`: DateTime (timestamp when conversation was created, auto-generated)
- `updated_at`: DateTime (timestamp of last activity, auto-updated)

**Relationships**:
- Belongs to one User (many-to-one)
- Has many Messages (one-to-many)

**Validation Rules**:
- `user_id` must reference an existing user
- `title` must be 1-255 characters if provided

### Message Entity
Represents individual exchanges in a conversation

**Fields**:
- `id`: UUID (Primary Key, auto-generated)
- `conversation_id`: UUID (Foreign Key to Conversation, cascading delete)
- `user_id`: UUID (Foreign Key to User, for reference)
- `role`: String (either "user" or "assistant", validates allowed values)
- `content`: Text (the actual message content, up to 10000 characters)
- `timestamp`: DateTime (when the message was sent, auto-generated)
- `metadata`: JSON (optional structured data about the message)

**Relationships**:
- Belongs to one Conversation (many-to-one)
- Belongs to one User (many-to-one)

**Validation Rules**:
- `conversation_id` must reference an existing conversation
- `user_id` must reference an existing user
- `role` must be either "user" or "assistant"
- `content` must be 1-10000 characters

## State Transitions

### Conversation States
- Active: New conversation created
- Updated: New messages added to conversation
- Closed: Conversation archived (future enhancement)

### Message States
- Pending: Message queued for processing (internal use)
- Sent: Message successfully saved to database
- Processed: Message handled by AI agent (for assistant messages)

## Indexes

### Required Database Indexes
- `conversation.user_id` - for user-based queries
- `conversation.created_at` - for chronological ordering
- `message.conversation_id` - for conversation-based queries
- `message.timestamp` - for chronological ordering within conversations
- Composite: `message.conversation_id` + `message.timestamp` - for efficient conversation history retrieval