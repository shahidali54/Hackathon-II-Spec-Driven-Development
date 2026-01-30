# Quickstart Guide: AI Chat Agent & Integration

## Overview
This guide explains how to set up and use the AI Chat Agent for task management in the TaskFlow application.

## Prerequisites
- OpenAI API key configured in environment variables
- MCP tools for task operations (defined as HTTP endpoints)
- JWT authentication system (Better Auth) properly configured

## Backend Setup

### 1. Environment Variables
```bash
# Add to your .env file
OPENAI_API_KEY=your_openai_api_key_here
MCP_TASKS_BASE_URL=http://localhost:8000/api/tasks
```

### 2. Database Models
The system includes two new database models:
- `Conversation`: Tracks chat sessions between users and AI
- `Message`: Stores individual exchanges in conversations

### 3. API Endpoints
- `POST /api/chat`: Main endpoint for chat interactions
- `GET /api/conversations`: Retrieve user's conversations
- `GET /api/conversations/{id}/messages`: Get messages from a conversation

## Frontend Integration

### 1. Chat Page
The chat interface is available at `/dashboard/chat` where users can:
- Interact with the AI agent using natural language
- View conversation history
- Manage multiple conversations

### 2. Authentication
The chat interface automatically passes JWT tokens to backend API calls for authentication.

## Using the AI Agent

### Natural Language Commands
Users can interact with the AI agent using commands like:
- "Add a task to buy groceries"
- "Show me my incomplete tasks"
- "Mark the grocery task as completed"
- "Delete the meeting task"

### Behind the Scenes
1. User sends message to `/api/chat`
2. System authenticates user and loads conversation context
3. AI agent interprets the request and determines required actions
4. AI agent calls MCP tools to perform task operations
5. System persists the conversation and returns response
6. Frontend displays the response to the user

## Security & User Isolation
- All operations are validated against the authenticated user
- Users can only access their own conversations and tasks
- MCP tools ensure proper authorization for all operations
- JWT tokens are validated on every request

## Troubleshooting
- If AI responses seem incorrect, check that the OpenAI API key is properly configured
- If conversations aren't persisting, verify database connection and permissions
- If authentication fails, ensure Better Auth is properly configured