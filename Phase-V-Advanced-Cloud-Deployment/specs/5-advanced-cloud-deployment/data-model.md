# Data Model: Implementation of Advanced & Intermediate Features for AI-Powered Todo Chatbot (Phase V - Part A)

**Feature**: Implementation of Advanced & Intermediate Features for AI-Powered Todo Chatbot
**Date**: 2026-02-09
**Author**: Claude
**Status**: Complete

## Overview

This document defines the extended data model for the AI-Powered Todo Chatbot with advanced and intermediate features. The model builds on the existing Phase II-IV data structures while adding support for priorities, tags, due dates, recurring tasks, and reminders.

## Core Entities

### Task

The primary entity for todo items, extended with new fields for advanced features.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier for the task |
| title | VARCHAR(255) | Not Null | Task title |
| description | TEXT | Nullable | Detailed description of the task |
| completed | BOOLEAN | Default False, Not Null | Whether the task is completed |
| priority | VARCHAR(20) | Enum ('low', 'medium', 'high', 'urgent'), Default 'medium' | Priority level of the task |
| tags | TEXT[] | Nullable | Array of tags associated with the task |
| due_date | TIMESTAMP WITH TIME ZONE | Nullable | Date and time when the task is due |
| recurrence_rule | JSONB | Nullable | JSON object defining the recurrence pattern |
| completed_at | TIMESTAMP WITH TIME ZONE | Nullable | Timestamp when the task was completed |
| created_by_user_id | UUID | Foreign Key, Not Null | ID of the user who created the task |
| created_at | TIMESTAMP WITH TIME ZONE | Default NOW(), Not Null | When the task was created |
| updated_at | TIMESTAMP WITH TIME ZONE | Default NOW(), Not Null | When the task was last updated |
| reminder_sent | BOOLEAN | Default False, Not Null | Flag to track if a reminder has been sent |

#### Validation Rules
- A task cannot have a due_date in the past if it's not completed
- The priority must be one of the allowed enum values
- If recurrence_rule is present, the task must be completable
- Tags must follow naming conventions (no special characters except hyphens and underscores)

#### Indexes
- `idx_task_user_id`: Index on created_by_user_id for efficient user filtering
- `idx_task_due_date`: Index on due_date for efficient due date queries
- `idx_task_priority`: Index on priority for efficient priority-based queries
- `idx_task_completed`: Index on completed for efficient completion status queries
- `idx_task_tags_gin`: GIN index on tags array for efficient tag-based queries
- `idx_task_created_at`: Index on created_at for efficient chronological queries

### RecurringTaskPattern

Entity to manage recurrence rules separately for better organization.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier for the recurrence pattern |
| task_id | UUID | Foreign Key, Not Null | Reference to the base task |
| rule | JSONB | Not Null | JSON object defining the recurrence rule (frequency, interval, end condition) |
| next_occurrence | TIMESTAMP WITH TIME ZONE | Nullable | When the next occurrence should be created |
| created_at | TIMESTAMP WITH TIME ZONE | Default NOW(), Not Null | When the pattern was created |
| updated_at | TIMESTAMP WITH TIME ZONE | Default NOW(), Not Null | When the pattern was last updated |

#### Validation Rules
- The rule must be a valid recurrence pattern
- The next_occurrence must be in the future when set

### Reminder

Entity to track scheduled reminders for tasks.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier for the reminder |
| task_id | UUID | Foreign Key, Not Null | Reference to the task being reminded |
| remind_at | TIMESTAMP WITH TIME ZONE | Not Null | When the reminder should be sent |
| sent | BOOLEAN | Default False, Not Null | Whether the reminder has been sent |
| sent_at | TIMESTAMP WITH TIME ZONE | Nullable | When the reminder was sent |
| created_at | TIMESTAMP WITH TIME ZONE | Default NOW(), Not Null | When the reminder was created |
| updated_at | TIMESTAMP WITH TIME ZONE | Default NOW(), Not Null | When the reminder was last updated |

#### Validation Rules
- remind_at must be in the future when created
- A task cannot have multiple active reminders

## Supporting Tables

### TaskEventLog (Optional)

Audit trail for all task operations (may be implemented if needed for compliance).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | Primary Key, Not Null | Unique identifier for the log entry |
| task_id | UUID | Foreign Key, Not Null | Reference to the affected task |
| user_id | UUID | Foreign Key, Not Null | User who performed the action |
| operation | VARCHAR(50) | Not Null | Type of operation (CREATE, UPDATE, DELETE, COMPLETE) |
| old_values | JSONB | Nullable | Previous state of the task before the operation |
| new_values | JSONB | Nullable | New state of the task after the operation |
| occurred_at | TIMESTAMP WITH TIME ZONE | Default NOW(), Not Null | When the event occurred |

## Relationships

```
User (1) -----> (Many) Task
Task (1) -----> (0..1) RecurringTaskPattern (via task_id)
Task (1) -----> (Many) Reminder (via task_id)
Task (1) -----> (Many) TaskEventLog (via task_id) [if implemented]
```

## State Transitions

### Task State Transition
- `CREATED` -> `COMPLETED` (when task.completed = true)
- `COMPLETED` -> `RECURRING_CREATED` (when a recurring task creates a new instance)
- `DUE_SOON` -> `REMINDER_SENT` (when reminder is sent before due date)
- `OVERDUE` -> `DUE_SOON` (when due date is updated)

### Reminder State Transition
- `SCHEDULED` -> `SENT` (when reminder is sent)
- `SENT` -> `FAILED` (if sending fails after retries)

## Database Schema

```sql
-- Extensions needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Task table
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    priority VARCHAR(20) NOT NULL DEFAULT 'medium' CHECK (priority IN ('low', 'medium', 'high', 'urgent')),
    tags TEXT[],
    due_date TIMESTAMP WITH TIME ZONE,
    recurrence_rule JSONB,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_by_user_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    reminder_sent BOOLEAN NOT NULL DEFAULT FALSE
);

-- Indexes for Task
CREATE INDEX idx_task_user_id ON tasks(created_by_user_id);
CREATE INDEX idx_task_due_date ON tasks(due_date);
CREATE INDEX idx_task_priority ON tasks(priority);
CREATE INDEX idx_task_completed ON tasks(completed);
CREATE INDEX idx_task_tags_gin ON tasks USING GIN(tags);
CREATE INDEX idx_task_created_at ON tasks(created_at);

-- RecurringTaskPattern table
CREATE TABLE recurring_task_patterns (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    rule JSONB NOT NULL,
    next_occurrence TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Reminder table
CREATE TABLE reminders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    remind_at TIMESTAMP WITH TIME ZONE NOT NULL,
    sent BOOLEAN NOT NULL DEFAULT FALSE,
    sent_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Indexes for Reminder
CREATE INDEX idx_reminder_task_id ON reminders(task_id);
CREATE INDEX idx_reminder_remind_at ON reminders(remind_at);
CREATE INDEX idx_reminder_sent ON reminders(sent);

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_recurring_task_patterns_updated_at
    BEFORE UPDATE ON recurring_task_patterns
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_reminders_updated_at
    BEFORE UPDATE ON reminders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

## Security Considerations

1. **Row-Level Security**: All queries must be filtered by `created_by_user_id` to ensure users can only access their own tasks
2. **Field-Level Security**: Sensitive fields should be protected even if a user gains access to the database
3. **Data Encryption**: Sensitive data at rest should be encrypted in accordance with security policies
4. **Audit Trail**: Important operations should be logged for security monitoring

## Performance Considerations

1. **Index Optimization**: Proper indexing on frequently queried fields (user_id, due_date, priority)
2. **Query Optimization**: Use parameterized queries to prevent SQL injection
3. **Connection Pooling**: Use connection pooling to optimize database connections
4. **Partitioning**: For large-scale deployments, consider table partitioning by date or user