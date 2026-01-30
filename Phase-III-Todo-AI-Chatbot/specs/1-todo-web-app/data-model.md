# Data Model: Todo Full-Stack Web Application

## Overview
This document defines the data models for the secure, multi-user todo web application. It outlines the entities, their attributes, relationships, and validation rules based on the feature requirements.

## Entity Definitions

### User Entity
**Description**: Represents an authenticated user in the system

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the user
- `email`: String (Unique, Indexed) - User's email address for authentication
- `hashed_password`: String - BCrypt hashed password
- `first_name`: String (Optional) - User's first name
- `last_name`: String (Optional) - User's last name
- `created_at`: DateTime - Timestamp when the user account was created
- `updated_at`: DateTime - Timestamp when the user account was last updated
- `is_active`: Boolean (Default: True) - Whether the user account is active

**Validation Rules**:
- Email must be a valid email format
- Email must be unique across all users
- Password must meet minimum security requirements (if validated at this layer)

**Relationships**:
- One-to-Many: User has many Tasks

### Task Entity
**Description**: Represents a todo item created by a user

**Fields**:
- `id`: UUID (Primary Key) - Unique identifier for the task
- `title`: String (Required) - Title of the task
- `description`: Text (Optional) - Detailed description of the task
- `is_completed`: Boolean (Default: False) - Whether the task is completed
- `due_date`: DateTime (Optional) - Deadline for the task
- `priority`: Integer (Enum: 1-5, Default: 3) - Priority level of the task (1=Lowest, 5=Highest)
- `user_id`: UUID (Foreign Key) - Reference to the owning user
- `created_at`: DateTime - Timestamp when the task was created
- `updated_at`: DateTime - Timestamp when the task was last updated

**Validation Rules**:
- Title must not be empty (length > 0)
- Title length must not exceed 255 characters
- Due date must be in the future (if provided)
- Priority must be between 1 and 5
- User_id must reference an existing user

**Relationships**:
- Many-to-One: Task belongs to one User

## State Transitions

### Task State Transitions
- **Active to Completed**: When user marks task as complete via PATCH /complete endpoint
- **Completed to Active**: When user unmarks task as complete via PATCH /complete endpoint

### User State Transitions
- **Inactive to Active**: When user account is reactivated
- **Active to Inactive**: When user account is deactivated

## Indexes and Performance Considerations

### Required Indexes
- User.email (Unique Index) - For efficient authentication lookups
- Task.user_id (Index) - For efficient user-specific task queries
- Task.created_at (Index) - For chronological sorting
- Task.is_completed (Index) - For filtering completed/incomplete tasks

### Query Patterns
- Retrieve all tasks for a specific user (filtered by user_id)
- Retrieve specific task by ID and user (for ownership verification)
- Update task completion status by ID and user
- Create new task for authenticated user

## Data Integrity Rules

### Ownership Enforcement
- All task operations must verify that the authenticated user owns the task
- Queries must filter by user_id to prevent cross-user data access
- Updates and deletions must verify user ownership before execution

### Referential Integrity
- Task.user_id must reference an existing User.id
- Deleting a user should cascade delete their tasks (or soft-delete approach)

### Access Control
- Unauthenticated requests should return 401 Unauthorized
- Requests for tasks not owned by the authenticated user should return 403 Forbidden
- Invalid JWT tokens should result in 401 Unauthorized responses

## API Representation

### User (API Response)
```json
{
  "id": "uuid-string",
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "is_active": true
}
```

### Task (API Response)
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

## Database Schema

### SQL Tables

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Tasks table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    due_date TIMESTAMP WITH TIME ZONE,
    priority INTEGER DEFAULT 3 CHECK (priority >= 1 AND priority <= 5),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);
CREATE INDEX idx_tasks_is_completed ON tasks(is_completed);
```

This data model satisfies all functional requirements while enforcing the security constraints required for multi-user isolation.