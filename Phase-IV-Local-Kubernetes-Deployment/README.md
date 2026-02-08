# Hackathon-II-Phase-III- Full Stack Todo with AI Chat Agent

This is a full-stack Todo application developed as part of a hackathon using spec-driven-development methodology. The application features a modern web interface with secure user authentication, robust task management capabilities, and an AI-powered chat assistant for natural language task management.

## Project Overview

This full-stack application consists of:
- **Frontend**: Next.js 16+ application with modern UI/UX
- **Backend**: FastAPI server with RESTful API endpoints
- **Database**: Neon Serverless PostgreSQL for persistent storage
- **Authentication**: JWT-based authentication system
- **AI Agent**: OpenAI Agents SDK integration for natural language task management
- **Architecture**: Clean separation of concerns with scalable design

## Features

### Frontend Capabilities
- **User Authentication**: Registration, login, and logout functionality
- **Protected Dashboard**: Personalized task management interface
- **Task Operations**: Create, read, update, and delete (CRUD) operations
- **Task Status Management**: Toggle task completion status
- **Responsive Design**: Mobile-first responsive interface
- **Route Protection**: Middleware for secure route access
- **AI Chat Interface**: Natural language task management via AI assistant

### Backend Capabilities
- **RESTful API**: Comprehensive endpoints for all application features
- **User Management**: Registration and authentication endpoints
- **Task Management**: Full CRUD operations for user tasks
- **Security**: JWT token validation and user identification
- **Pagination**: Support for paginated task retrieval
- **Database Integration**: SQLModel ORM with Neon PostgreSQL
- **AI Agent Integration**: Dedicated chat API for AI agent communication
- **Conversation Management**: Persistent conversations and messages

### AI Agent Capabilities (Phase III)
- **Natural Language Processing**: Create, read, update, and delete tasks using natural language
- **MCP Tools Integration**: Secure task operations via existing backend APIs
- **Conversation Continuity**: Persistent conversations with context preservation
- **User Isolation**: Proper authentication and authorization for all operations
- **Response Validation**: Secure tool validation and response handling

### Authentication Flow
1. User authenticates through the frontend
2. Backend validates credentials and issues JWT tokens
3. Tokens are stored securely on the frontend
4. Subsequent API requests include the token in headers
5. Backend verifies token authenticity for protected endpoints
6. Only user-specific data is accessible per session
7. AI agent operations are authenticated and authorized through the same system

## Tech Stack

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Authentication**: Better Auth
- **Forms**: React Hook Form

### Backend
- **Framework**: FastAPI (Python)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT tokens with jose library
- **Validation**: Pydantic models
- **AI Agent**: OpenAI Agents SDK

### Development & Deployment
- **Methodology**: Spec-driven-development
- **Version Control**: Git
- **Package Management**: npm (frontend), pip (backend)

## Project Structure

```
Hackathon-II-Phase-III--Full-Stack-Todo/
├── frontend/                 # Next.js frontend application
│   ├── app/                  # Application routes and pages
│   ├── components/           # Reusable UI components
│   ├── hooks/                # Custom React hooks
│   ├── lib/                  # Utility functions
│   ├── middleware.ts         # Route protection middleware
│   ├── package.json          # Frontend dependencies
│   └── ...
├── backend/                  # FastAPI backend server
│   ├── src/
│   │   ├── api/              # API route definitions
│   │   │   ├── auth.py       # Authentication endpoints
│   │   │   ├── tasks.py      # Task management endpoints
│   │   │   ├── chat.py       # AI chat agent endpoints
│   │   │   ├── conversations.py  # Conversation management endpoints
│   │   │   └── conversation_messages.py  # Conversation messages endpoints
│   │   ├── database/         # Database connection and configuration
│   │   ├── models/           # Data models (SQLModel)
│   │   │   ├── task.py       # Task model
│   │   │   ├── user.py       # User model
│   │   │   ├── conversation.py  # Conversation model
│   │   │   └── message.py    # Message model
│   │   ├── services/         # Business logic implementations
│   │   │   ├── task_service.py  # Task business logic
│   │   │   ├── conversation_service.py  # Conversation business logic
│   │   │   └── message_service.py  # Message business logic
│   │   ├── tools/            # MCP tools for AI agent
│   │   │   └── task_tools.py # Task operation tools for AI agent
│   │   ├── agents/           # AI agent implementations
│   │   │   └── todo_agent.py # AI todo management agent
│   │   └── main.py           # Main application entry point
│   ├── requirements.txt      # Backend dependencies
│   └── ...
├── specs/                    # Specification-driven development artifacts
├── history/                  # Development history and records
├── .specify/                 # Spec-Kit Plus configurations
├── CLAUDE.md                 # Claude Code configuration
└── README.md                 # This file
```

## Getting Started

### Prerequisites
- Node.js (v18+)
- Python (v3.9+)
- PostgreSQL-compatible database (Neon recommended)
- OpenAI API key for AI agent functionality

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Hackathon-II-Phase-III--Full-Stack-Todo
   ```

2. **Setup Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   # Configure database connection and OpenAI API key in .env file
   python -m src.main  # Start the backend server (runs on port 8000)
   ```

3. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   # Configure environment variables in .env.local
   npm run dev  # Start the frontend server (runs on port 3000)
   ```

4. **Access the Application**
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - Backend API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Tasks
- `GET /api/tasks` - Retrieve user tasks (with optional filtering)
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Retrieve a specific task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

### AI Chat Agent (Phase III)
- `POST /api/chat` - Send message to AI agent and receive response
- `GET /api/conversations` - Retrieve user's conversations
- `GET /api/conversations/{conversation_id}/messages` - Retrieve messages from a conversation

## Security Features
- JWT token-based authentication
- User-specific data isolation
- Input validation and sanitization
- Secure session management
- Protected API endpoints
- AI agent operations secured through same authentication system
- MCP tools validation for AI agent actions

## Phase III: AI Chat Agent Integration

### AI Agent Capabilities
The application now includes an AI-powered chat assistant that enables natural language task management:

1. **Access the Chat Interface**:
   - Navigate to the dashboard after logging in
   - Click the "AI Chat Assistant" button to access the chat interface

2. **Natural Language Commands**:
   - "Add a task: Buy groceries" - Creates a new task
   - "Show me my tasks" - Displays current tasks
   - "Mark the grocery task as completed" - Updates task status
   - "Delete the meeting task" - Removes a task

3. **Under the Hood**:
   - AI agent uses OpenAI Agents SDK for processing
   - MCP tools ensure secure interaction with existing task APIs
   - All operations maintain proper user authentication and isolation
   - Conversations are persisted for context continuity

### AI Agent Architecture
- **OpenAI Agents SDK**: Powers the AI chat functionality
- **MCP Tools**: Secure interface between AI agent and task management system
- **Persistent Storage**: Conversations and messages stored in database
- **Authentication Integration**: Same JWT-based security as existing system

## Development Approach

This project was developed using the **Spec-Driven Development (SDD)** methodology:
- Comprehensive specifications created before implementation
- Detailed architectural planning
- Task breakdown with acceptance criteria
- Iterative development with continuous validation
- Prompt History Records (PHRs) for tracking decisions
- Phase III: AI agent integration following SDK patterns and best practices

## Contributing

This project was developed as part of a hackathon and follows the spec-driven-development approach. Contributions should maintain the established architecture and follow the original specifications. For Phase III features, ensure AI agent integration follows OpenAI Agents SDK patterns and maintains security standards.

## License

This project is part of Hackathon-II-Phase-III created using spec-driven-development methodology.