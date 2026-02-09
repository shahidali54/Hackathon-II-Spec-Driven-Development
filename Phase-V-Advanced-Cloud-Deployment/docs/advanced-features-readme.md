# Phase V Advanced Features Documentation

## Overview
This document describes the advanced features implemented in Phase V of the AI-Powered Todo Chatbot, including Recurring Tasks, Due Dates & Reminders, Priorities, Tags, Search, Filter, and Sort functionality.

## Features

### 1. Recurring Tasks
- Users can create tasks that repeat on a schedule (daily, weekly, monthly, yearly)
- Automatically generates new instances when the current one is marked complete
- Supports various recurrence patterns with end conditions

### 2. Due Dates & Reminders
- Users can assign due dates to tasks
- Configurable reminder settings to receive notifications before deadlines
- Event-driven architecture using Kafka for reliable reminder delivery

### 3. Task Priorities
- Four priority levels: Low, Medium, High, Urgent
- Visual indicators for priority levels in the UI
- Sorting and filtering by priority

### 4. Tags / Labels
- Users can categorize tasks with custom tags
- Efficient tag-based filtering and search
- Support for multiple tags per task

### 5. Advanced Search & Filter
- Full-text search across task titles and descriptions
- Filter by multiple criteria simultaneously (priority, tags, due dates, completion status)
- Sort by various properties (due date, priority, creation date, title)

### 6. Event-Driven Architecture
- Kafka integration for handling asynchronous operations
- Decoupled services with reliable event processing
- Supports real-time notifications and audit trails

### 7. Dapr Integration
- Distributed application runtime for service-to-service communication
- Pub/Sub messaging using Kafka
- State management and secret handling

## Architecture

### Backend Services
- **Main API Service**: Handles all CRUD operations and authenticates requests
- **Recurring Task Service**: Processes task completion events and creates next instances
- **Notification Service**: Handles time-sensitive reminder delivery

### Data Model Extensions
The Task model has been extended with:
- `priority`: ENUM for priority levels
- `tags`: Array of text tags
- `due_date`: DateTime for task deadlines
- `recurrence_rule`: JSON for recurrence patterns
- `reminder_sent`: Boolean flag for tracking reminder status

### API Endpoints
- `GET /api/tasks?priority=&tags=&due_date_from=&due_date_to=&search=&sort=&order=` - Enhanced filtering
- `GET /api/tasks/search?q=` - Dedicated search endpoint
- `GET /api/tasks/filter` - Advanced filtering by multiple criteria

## Kafka Event Flows

### Task Events Topic
- `task-created`: When a new task is created
- `task-updated`: When a task is updated
- `task-completion-toggled`: When task completion status changes
- `task-deleted`: When a task is deleted

### Reminders Topic
- `reminder-triggered`: When a reminder should be sent

### Task Updates Topic
- `recurring-task-generated`: When a recurring task creates a new instance

## Dapr Components

### Pub/Sub
- Kafka pubsub component for event-driven communication

### State Store
- PostgreSQL state store for durable state management

### Secret Store
- Local file-based secret store for sensitive configuration

## Security Considerations
- All new endpoints require valid JWT authentication
- User isolation maintained across all new features
- Input validation applied to all new fields
- Database queries filtered by authenticated user

## Development Setup

### Dependencies
- Python 3.11+
- Kafka (for event-driven architecture)
- Dapr runtime
- PostgreSQL with pgcrypto extension

### Environment Variables
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka broker addresses
- `DAPR_HTTP_PORT`: Dapr sidecar HTTP port
- `DAPR_GRPC_PORT`: Dapr sidecar gRPC port

## Testing
- Unit tests for all new services and utilities
- Integration tests for event flows
- End-to-end tests for complete user journeys
- Performance tests for search and filter operations

## Deployment
The system is designed for cloud deployment with:
- Containerized services
- Dapr for portable distributed runtime
- Kafka for reliable event processing
- PostgreSQL for persistent storage