# Quickstart Guide: Authentication & Security Implementation

## Overview
This guide provides essential information to implement JWT-based authentication and security features using Better Auth for Next.js frontend and FastAPI backend.

## Prerequisites
- Node.js 18+ (for Next.js frontend)
- Python 3.11+ (for FastAPI backend)
- PostgreSQL-compatible database (Neon Serverless PostgreSQL recommended)
- Understanding of the existing Todo application structure

## Setup Instructions

### 1. Update Backend Dependencies
```bash
# Navigate to backend directory
cd backend

# Update requirements.txt with authentication dependencies
# Already included in the existing requirements.txt:
# python-jose[cryptography]==3.3.0
# passlib[bcrypt]==1.7.4
# python-multipart==0.0.6
# pyjwt==2.8.0

# Install dependencies
pip install -r requirements.txt
```

### 2. Update Environment Variables
```bash
# In backend/.env, add:
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Update Frontend Dependencies
```bash
# Navigate to frontend directory
cd frontend

# Install authentication dependencies if not already installed
npm install better-auth axios
```

## Authentication Implementation Steps

### 1. Backend JWT Implementation
1. **Update auth endpoints** in `backend/src/api/auth.py`:
   - Add JWT token generation on login
   - Add JWT verification dependency
   - Update user registration to return JWT

2. **Create JWT utilities** in `backend/src/utils/security.py`:
   - Functions to create and verify JWT tokens
   - User extraction from JWT
   - Token validation logic

3. **Update secured endpoints** in `backend/src/api/tasks.py`:
   - Add JWT dependency to all endpoints
   - Modify endpoints to use user ID from JWT instead of URL
   - Add proper 401 and 403 responses

### 2. Frontend Authentication Implementation
1. **Update API client** in `frontend/src/lib/api.ts`:
   - Add JWT token to all requests
   - Handle 401 responses with redirect to login
   - Token storage and retrieval

2. **Create auth utilities** in `frontend/src/lib/auth.ts`:
   - Login/logout functions
   - Token management
   - Session checking

3. **Update UI components**:
   - Add ProtectedRoute component
   - Update task components to use auth context

## Key Implementation Details

### JWT Token Flow
1. User signs in via frontend
2. Backend verifies credentials and creates JWT
3. JWT is returned to frontend
4. Frontend stores JWT and includes in Authorization header
5. Backend verifies JWT on each protected request
6. User identity is extracted from JWT claims
7. All data access is filtered by authenticated user

### Security Measures
- JWT tokens are stateless and self-contained
- User ID is extracted from JWT, not URL parameters
- All database queries are filtered by authenticated user
- Proper error responses (401/403) for unauthorized access
- Tokens have configurable expiration times

### Environment Variables

#### Backend (.env)
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_SECRET=your-super-secret-jwt-key-here
NEXTAUTH_URL=http://localhost:3000
```

## API Endpoints with Authentication

### Authentication Endpoints
- `POST /api/auth/register` - Register new user and return JWT
- `POST /api/auth/login` - Login and return JWT token
- `POST /api/auth/logout` - Logout user (optional for JWT)

### Secured Task API Endpoints (now using JWT instead of user_id in URL)
- `GET /api/tasks` - Get all tasks for authenticated user
- `POST /api/tasks` - Create new task for authenticated user
- `GET /api/tasks/{id}` - Get specific task for authenticated user
- `PUT /api/tasks/{id}` - Update task for authenticated user
- `DELETE /api/tasks/{id}` - Delete task for authenticated user
- `PATCH /api/tasks/{id}/complete` - Toggle task completion for authenticated user

## Testing Authentication

### Manual Testing Steps
1. Register a new user
2. Verify JWT token is returned
3. Make API calls with JWT in Authorization header
4. Verify 401 response for requests without token
5. Attempt to access another user's data and verify 403 response
6. Test token expiration handling

### Common Issues
1. **JWT Validation Errors**: Ensure BETTER_AUTH_SECRET matches between components
2. **Token Not Attached**: Check that API client includes Authorization header
3. **User Isolation**: Verify endpoints use JWT user ID, not URL parameter
4. **CORS Issues**: Check that frontend URL is allowed in backend settings

## Next Steps

1. Implement the JWT creation and verification functions
2. Update all existing endpoints to use JWT authentication
3. Modify frontend to store and send JWT tokens
4. Test the complete authentication flow
5. Verify user isolation and security measures
6. Update documentation with new authentication flows