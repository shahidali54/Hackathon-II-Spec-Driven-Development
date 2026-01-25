# Hackathon-II-Phase-II- Full Stack Todo

This is a full-stack Todo application developed as part of a hackathon using spec-driven-development methodology. The application features a modern web interface with secure user authentication and robust task management capabilities.

## Project Overview

This full-stack application consists of:
- **Frontend**: Next.js 16+ application with modern UI/UX
- **Backend**: FastAPI server with RESTful API endpoints
- **Database**: Neon Serverless PostgreSQL for persistent storage
- **Authentication**: JWT-based authentication system
- **Architecture**: Clean separation of concerns with scalable design

## Features

### Frontend Capabilities
- **User Authentication**: Registration, login, and logout functionality
- **Protected Dashboard**: Personalized task management interface
- **Task Operations**: Create, read, update, and delete (CRUD) operations
- **Task Status Management**: Toggle task completion status
- **Responsive Design**: Mobile-first responsive interface
- **Route Protection**: Middleware for secure route access

### Backend Capabilities
- **RESTful API**: Comprehensive endpoints for all application features
- **User Management**: Registration and authentication endpoints
- **Task Management**: Full CRUD operations for user tasks
- **Security**: JWT token validation and user identification
- **Pagination**: Support for paginated task retrieval
- **Database Integration**: SQLModel ORM with Neon PostgreSQL

### Authentication Flow
1. User authenticates through the frontend
2. Backend validates credentials and issues JWT tokens
3. Tokens are stored securely on the frontend
4. Subsequent API requests include the token in headers
5. Backend verifies token authenticity for protected endpoints
6. Only user-specific data is accessible per session

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

### Development & Deployment
- **Methodology**: Spec-driven-development
- **Version Control**: Git
- **Package Management**: npm (frontend), pip (backend)

## Project Structure

```
Hackathon-II-Phase-II--Full-Stack-Todo/
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
│   │   ├── database/         # Database connection and configuration
│   │   ├── models/           # Data models (SQLModel)
│   │   ├── services/         # Business logic implementations
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

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Hackathon-II-Phase-II--Full-Stack-Todo
   ```

2. **Setup Backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   # Configure database connection in .env file
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

## Security Features
- JWT token-based authentication
- User-specific data isolation
- Input validation and sanitization
- Secure session management
- Protected API endpoints

## Development Approach

This project was developed using the **Spec-Driven Development (SDD)** methodology:
- Comprehensive specifications created before implementation
- Detailed architectural planning
- Task breakdown with acceptance criteria
- Iterative development with continuous validation
- Prompt History Records (PHRs) for tracking decisions

## Contributing

This project was developed as part of a hackathon and follows the spec-driven-development approach. Contributions should maintain the established architecture and follow the original specifications.

## License

This project is part of Hackathon-II-Phase-II created using spec-driven-development methodology.