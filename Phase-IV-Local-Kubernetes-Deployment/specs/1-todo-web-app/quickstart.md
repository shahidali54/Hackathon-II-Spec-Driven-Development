# Quickstart Guide: Todo Full-Stack Web Application

## Overview
This guide provides essential information to quickly set up and run the Todo Full-Stack Web Application with authentication and multi-user support.

## Prerequisites
- Node.js 18+ (for Next.js frontend)
- Python 3.11+ (for FastAPI backend)
- PostgreSQL-compatible database (Neon Serverless PostgreSQL recommended)
- Docker (optional, for containerized development)

## Setup Instructions

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup (FastAPI)
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your database URL and BETTER_AUTH_SECRET

# Run database migrations
alembic upgrade head

# Start the backend server
uvicorn src.main:app --reload --port 8000
```

### 3. Frontend Setup (Next.js)
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set environment variables
cp .env.local.example .env.local
# Edit .env.local with your backend API URL and auth settings

# Start the development server
npm run dev
```

## Environment Variables

### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_SECRET=your-super-secret-jwt-key-here
NEXTAUTH_URL=http://localhost:3000
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `POST /api/auth/logout` - Logout user

### Tasks API
- `GET /api/{user_id}/tasks` - Get all tasks for user
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Authentication Flow

1. User registers/signs in via frontend
2. Better Auth generates JWT token
3. Frontend stores token and includes in Authorization header
4. Backend validates JWT and extracts user ID
5. Backend verifies user ownership of requested resources
6. Appropriate response returned based on permissions

## Database Models

### User
- id (UUID, Primary Key)
- email (String, Unique)
- hashed_password (String)
- first_name, last_name (Optional Strings)
- timestamps and active status

### Task
- id (UUID, Primary Key)
- title (String, Required)
- description (Text, Optional)
- is_completed (Boolean, Default: False)
- due_date, priority (Optional fields)
- user_id (UUID, Foreign Key)
- timestamps

## Running Tests

### Backend Tests
```bash
# From backend directory
pytest tests/ -v
```

### Frontend Tests
```bash
# From frontend directory
npm run test
```

## Development Commands

### Backend
- `uvicorn src.main:app --reload` - Start dev server with auto-reload
- `alembic revision --autogenerate -m "description"` - Generate migration
- `alembic upgrade head` - Apply migrations

### Frontend
- `npm run dev` - Start dev server
- `npm run build` - Build for production
- `npm run start` - Start production server

## Common Issues

1. **JWT Validation Errors**: Ensure BETTER_AUTH_SECRET matches between frontend and backend
2. **Database Connection**: Verify DATABASE_URL is properly configured
3. **CORS Issues**: Check that frontend URL is allowed in backend settings
4. **User Ownership**: Remember that user_id in URL is validated against JWT token

## Next Steps

1. Complete the user registration flow
2. Implement the main task management UI
3. Add additional features as per requirements
4. Test the complete authentication and authorization flow
5. Deploy to staging environment for further testing