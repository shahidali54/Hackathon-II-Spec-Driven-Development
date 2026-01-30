# Data Model: Frontend Web Application

## Overview
This document defines the frontend data models for the Next.js frontend application. It outlines the data structures, their attributes, relationships, and validation rules based on the feature requirements. The models represent the shape of data as it flows through the frontend application.

## Entity Definitions

### User Entity (Frontend)
**Description**: Represents an authenticated user in the frontend application state

**Fields**:
- `id`: string - Unique identifier for the user
- `email`: string - User's email address for authentication
- `first_name`: string (Optional) - User's first name
- `last_name`: string (Optional) - User's last name
- `is_active`: boolean (Default: True) - Whether the user account is active
- `created_at`: string (ISO date-time) - Timestamp when the user account was created
- `updated_at`: string (ISO date-time) - Timestamp when the user account was last updated

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users

**Relationships**:
- One-to-Many: User has many Tasks (in frontend state)

### Task Entity (Frontend)
**Description**: Represents a todo item managed by the frontend application

**Fields**:
- `id`: string - Unique identifier for the task
- `title`: string - Title of the task (required, max 255 chars)
- `description`: string (Optional) - Detailed description of the task
- `is_completed`: boolean (Default: False) - Whether the task is completed
- `due_date`: string (ISO date-time, Optional) - Deadline for the task
- `priority`: number (Enum: 1-5, Default: 3) - Priority level of the task (1=Lowest, 5=Highest)
- `user_id`: string - Reference to the owning user
- `created_at`: string (ISO date-time) - Timestamp when the task was created
- `updated_at`: string (ISO date-time) - Timestamp when the task was last updated

**Validation Rules**:
- Title must not be empty (length > 0)
- Title length must not exceed 255 characters
- Due date must be in the future (if provided)
- Priority must be between 1 and 5
- User_id must reference an existing user in the frontend state

**Relationships**:
- Many-to-One: Task belongs to one User

### AuthSession Entity (Frontend)
**Description**: Represents an active authentication session in the frontend application

**Fields**:
- `access_token`: string - JWT token for API authentication
- `token_type`: string (Default: "bearer") - Type of authentication token
- `expires_in`: number - Time in seconds until token expires
- `expires_at`: string (ISO date-time) - Absolute time when token expires
- `user`: User - Associated user object
- `is_authenticated`: boolean - Whether the session is currently valid

**Validation Rules**:
- Access token must be a valid JWT format
- Expires_at must be in the future
- User object must be valid

## State Management Patterns

### Global State Structure
The frontend application will use React Context API for global state management with the following structure:

```typescript
interface AppState {
  auth: AuthSession | null;
  tasks: Task[];
  loading: boolean;
  error: string | null;
}
```

### Component State Patterns
Individual components will manage their own UI-specific state:
- Form inputs: Controlled components with local state
- Modal/open states: Boolean flags for UI elements
- Loading states: Per-request loading indicators

## API Response Types

### Authentication Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Task List Response
```json
{
  "tasks": [
    {
      "id": "uuid-string",
      "title": "Sample Task",
      "description": "Detailed description of the task",
      "is_completed": false,
      "due_date": "2023-12-31T23:59:59Z",
      "priority": 3,
      "user_id": "user-uuid-string",
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ],
  "total": 1
}
```

### Individual Task Response
```json
{
  "id": "uuid-string",
  "title": "Sample Task",
  "description": "Detailed description of the task",
  "is_completed": false,
  "due_date": "2023-12-31T23:59:59Z",
  "priority": 3,
  "user_id": "user-uuid-string",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

## Form Data Structures

### User Registration Form
```typescript
interface UserRegistrationForm {
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
}
```

### Task Creation Form
```typescript
interface TaskCreationForm {
  title: string;
  description?: string;
  due_date?: string;
  priority?: number;
}
```

### Task Update Form
```typescript
interface TaskUpdateForm {
  title?: string;
  description?: string;
  is_completed?: boolean;
  due_date?: string;
  priority?: number;
}
```

## Validation Rules

### Frontend Validation
- Email format validation using standard regex patterns
- Password strength validation (minimum length, character requirements)
- Task title length validation (max 255 characters)
- Date validation (due dates must be in the future)
- Priority range validation (1-5 scale)

### Error Handling
- Form validation errors displayed inline with inputs
- API error messages displayed in user-friendly format
- Loading states during async operations
- Network error handling with retry mechanisms

## API Interaction Patterns

### Request Structure
- All authenticated requests include Authorization header: `Bearer {access_token}`
- JSON content-type for request bodies
- Proper error handling for different HTTP status codes

### Response Handling
- Successful responses update frontend state
- 401 responses trigger logout and redirect to login
- 403 responses show permission error
- 4xx/5xx responses show appropriate error messages

This data model ensures the frontend application properly manages user authentication, task data, and API interactions while maintaining consistency with the backend data structures.