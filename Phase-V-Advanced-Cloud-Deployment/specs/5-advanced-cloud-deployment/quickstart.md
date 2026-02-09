# Quickstart Guide: Implementation of Advanced & Intermediate Features for AI-Powered Todo Chatbot (Phase V - Part A)

**Feature**: Implementation of Advanced & Intermediate Features for AI-Powered Todo Chatbot
**Date**: 2026-02-09
**Author**: Claude
**Status**: Complete

## Overview

This guide provides essential setup instructions for implementing the advanced and intermediate features for the AI-Powered Todo Chatbot, including Kafka for event-driven architecture and Dapr for distributed runtime capabilities.

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm/yarn
- Docker and Docker Compose
- Dapr CLI installed globally
- Access to a Kafka cluster (Redpanda Cloud or local setup)
- PostgreSQL database (Neon Serverless or local instance)

## Environment Setup

### 1. Install Dependencies

```bash
# Install Python dependencies for backend
pip install -r backend/requirements.txt

# Install Node.js dependencies for frontend
cd frontend
npm install
cd ..

# Install Dapr (if not already installed)
# Visit https://docs.dapr.io/getting-started/install-dapr-cli/ for instructions
```

### 2. Configure Environment Variables

Create `.env` files in both backend and frontend directories:

**Backend (.env)**:
```env
DATABASE_URL=postgresql://username:password@host:port/dbname
BETTER_AUTH_SECRET=your-secret-key
BETTER_AUTH_URL=http://localhost:3000
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC_TASK_EVENTS=task-events
KAFKA_TOPIC_REMINDERS=reminders
KAFKA_TOPIC_TASK_UPDATES=task-updates
DAPR_HTTP_PORT=3500
DAPR_GRPC_PORT=50001
```

**Frontend (.env.local)**:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BASE_PATH=/api
```

### 3. Start Dapr Components

Create Dapr configuration files in the `backend/dapr` directory:

**backend/dapr/config.yaml**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: daprconfig
spec:
  tracing:
    samplingRate: "1"
    zipkin:
      endpointAddress: "http://zipkin.default.svc.cluster.local:9411/api/v1/spans"
```

**backend/dapr/components/pubsub.yaml**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "localhost:9092"
  - name: consumerGroup
    value: "dapr-kafka-consumer-group"
  - name: clientID
    value: "dapr-kafka-client"
  - name: authType
    value: "none"
```

**backend/dapr/components/statestore.yaml**:
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: postgres-state-store
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    value: "postgresql://username:password@localhost:5432/postgres"
  - name: versionColumnType
    value: "version"
```

## Starting Services

### 1. Start Kafka Locally (for development)

```bash
# Using Docker Compose
docker-compose -f .kafka/docker-compose.yml up -d
```

### 2. Initialize Dapr

```bash
# Start Dapr locally
dapr init

# Verify installation
dapr --version
```

### 3. Run the Backend Service

```bash
# Navigate to backend directory
cd backend

# Start Dapr with the backend app
dapr run --app-id todo-backend --app-port 8000 --dapr-http-port 3500 -- python src/main.py
```

### 4. Run the Frontend Service

```bash
# In a separate terminal
cd frontend
npm run dev
```

### 5. Start the Recurring Task Service

```bash
# In a separate terminal
cd services/recurring-task-service
dapr run --app-id recurring-task-service -- python app.py
```

### 6. Start the Notification Service

```bash
# In a separate terminal
cd services/notification-service
dapr run --app-id notification-service -- python app.py
```

## Running Tests

### Backend Tests
```bash
# Run unit tests
python -m pytest tests/unit/

# Run integration tests
python -m pytest tests/integration/

# Run contract tests
python -m pytest tests/contract/
```

### Frontend Tests
```bash
# Run frontend tests
cd frontend
npm test
```

## Key Endpoints

### Main API (Backend)
- `GET /api/tasks` - Retrieve user's tasks
- `POST /api/tasks` - Create a new task with priority, tags, due_date, recurrence_rule
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `POST /api/tasks/{id}/complete` - Complete a task and trigger recurrence if applicable
- `GET /api/tasks/search?q=searchTerm` - Search tasks
- `GET /api/tasks/filter?priority=high&due_date_from=2023-01-01` - Filter tasks

### Dapr Sidecar Endpoints
- `POST http://localhost:3500/v1.0/invoke/todo-backend/method/api/tasks` - Invoke backend API via Dapr
- `POST http://localhost:3500/v1.0/publish/kafka-pubsub/task-events` - Publish events to Kafka

## Development Workflow

### 1. Making Changes to the Task Model
- Update `src/models/task.py` with new fields
- Update `src/schemas/task.py` with Pydantic schemas
- Update the database migration files
- Update frontend components to handle new fields

### 2. Adding Kafka Events
- Define the event structure in `src/services/kafka_producer.py`
- Publish events when specific actions occur (task completion, creation, etc.)
- Create handlers in the Recurring Task and Notification Services

### 3. Updating Dapr Components
- Modify the configuration files in the `dapr/components` directory
- Restart Dapr services after changes

### 4. Testing Event Flow
1. Create a task with a due date and reminder settings
2. Monitor Kafka topics for reminder events
3. Verify that the Notification Service processes the events
4. For recurring tasks, complete a task and verify that a new instance is created

## Common Commands

```bash
# Reset Dapr
dapr uninstall
dapr init

# Check running Dapr apps
dapr list

# Get Dapr logs
dapr logs <app-id>

# Send a test event to Kafka via Dapr
curl -X POST http://localhost:3500/v1.0/publish/kafka-pubsub/task-events \
  -H "Content-Type: application/json" \
  -d '{"taskId": "123", "event": "taskCompleted"}'

# Check Kafka topics
docker exec -it kafka-container kafka-topics --bootstrap-server localhost:9092 --list
```

## Troubleshooting

### Issues with Dapr
- If Dapr services aren't communicating, verify that the app IDs match the configuration
- Check that the Dapr ports (3500, 50001) are available
- Use `dapr logs <app-id>` to view service logs

### Issues with Kafka
- Verify that Kafka is running and accessible
- Check that the required topics are created
- Look for authentication issues if connecting to Redpanda Cloud

### Database Connection Issues
- Verify that the DATABASE_URL is correct
- Check that PostgreSQL is running and accessible
- Ensure that the required extensions are enabled (UUID, pgcrypto)

## Next Steps

1. Implement the Recurring Task Service logic to process completion events and create new instances
2. Implement the Notification Service to handle reminder events and send notifications
3. Update frontend components to support new task properties (priority, tags, due date, recurrence)
4. Implement search, filter, and sort functionality in both backend and frontend
5. Connect the new features to the MCP tools for AI chatbot integration