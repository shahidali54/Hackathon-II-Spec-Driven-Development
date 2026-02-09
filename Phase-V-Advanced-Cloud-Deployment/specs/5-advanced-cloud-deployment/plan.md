# Implementation Plan: Implementation of Advanced & Intermediate Features for AI-Powered Todo Chatbot (Phase V - Part A)

**Branch**: `5-advanced-cloud-deployment` | **Date**: 2026-02-09 | **Spec**: [link](spec.md)

**Input**: Feature specification from `/specs/5-advanced-cloud-deployment/spec.md`

## Summary

Implement all required features for Advanced & Intermediate levels (Recurring Tasks, Due Dates & Reminders, Priorities, Tags, Search, Filter, Sort) with event-driven architecture using Kafka and distributed runtime using Dapr. The implementation will build on the existing Phase II-IV codebase while maintaining backward compatibility.

## Technical Context

**Language/Version**: Python 3.11, JavaScript/TypeScript for Next.js
**Primary Dependencies**: FastAPI, SQLModel, Next.js 16+, Better Auth, confluent-kafka/python, dapr-sdk for Python, OpenAI Agents SDK
**Storage**: Neon Serverless PostgreSQL
**Testing**: pytest for backend, Jest for frontend
**Target Platform**: Linux server, web browser
**Project Type**: Web application with distributed services
**Performance Goals**: 80% unit test coverage, <500ms search response, <200ms API response
**Constraints**: Maintain backward compatibility with Phases I-IV, use additive schema changes only, <1 min reminder delivery

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Verification
- [X] **Correctness**: Implementation will match defined requirements exactly
- [X] **Security-first**: Authentication, authorization, and data isolation will be mandatory
- [X] **Spec-driven**: Development will follow Spec-Kit Plus and Claude Code workflows
- [X] **Simplicity**: Solutions will prioritize clarity and maintainability
- [X] **Reliability**: System will behave consistently across frontend and backend
- [X] **API Design**: Endpoints will be fully RESTful with proper HTTP status codes
- [X] **Data Integrity**: All task operations will enforce user ownership
- [X] **Tech Stack**: Will use Next.js 16+, FastAPI, SQLModel, Neon PostgreSQL, Better Auth, Kafka, Dapr
- [X] **Authentication**: All endpoints will require valid JWT tokens after auth integration
- [X] **Security Rules**: JWT tokens will be verified using shared secret, user identification from token, DB queries filtered by authenticated user
- [X] **Behavior Constraints**: Users will only see/modify their own tasks, invalid access returns 403, missing/invalid tokens return 401
- [X] **Event-driven Architecture**: Kafka will be used for all asynchronous operations
- [X] **Dapr Integration**: Will be used for pub/sub, state management, service invocation, and secrets
- [X] **Backward Compatibility**: Will ensure all new features maintain compatibility with Phases I-IV

## Project Structure

### Documentation (this feature)

```text
specs/5-advanced-cloud-deployment/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py           # Updated with new fields (priority, tags, due_date, recurring_rule)
│   │   └── user.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── task_service.py   # Updated with search, filter, sort logic
│   │   ├── recurring_service.py  # New service for recurring tasks
│   │   ├── reminder_service.py   # New service for reminders
│   │   └── kafka_producer.py     # New service for Kafka events
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   ├── auth.py
│   │   └── tasks.py        # Updated with new endpoints
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── task.py         # Updated with new fields
│   └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
├── requirements.txt      # Updated with Kafka, Dapr dependencies
├── Dockerfile
└── dapr/
    ├── components/
    │   ├── pubsub.yaml     # Kafka pub/sub component
    │   ├── statestore.yaml # Dapr state store
    │   └── secrets.yaml    # Dapr secrets store
    └── config.yaml

frontend/
├── src/
│   ├── components/
│   │   ├── TaskForm.jsx      # Updated with priority, tags, due_date, recurring inputs
│   │   ├── TaskList.jsx      # Updated with search, filter, sort UI
│   │   ├── PrioritySelector.jsx
│   │   ├── TagManager.jsx
│   │   └── DatePicker.jsx
│   ├── pages/
│   │   └── dashboard/
│   │       └── index.jsx
│   ├── services/
│   │   ├── api.js
│   │   └── task-api.js     # Updated with new functionality
│   └── utils/
│       └── helpers.js
├── package.json            # Updated with any new dependencies
└── next.config.js

services/
├── recurring-task-service/     # Separate Dapr-enabled service
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── notification-service/       # Separate Dapr-enabled service
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
└── dapr-config/              # Shared Dapr configuration

.kafka/
├── topics/
│   ├── task-events.json
│   ├── reminders.json
│   └── task-updates.json
└── docker-compose.yml         # For local Kafka development

README.md                     # Updated with architecture diagram and new features
```

**Structure Decision**: Multi-service architecture with backend API, separate Dapr-enabled services for recurring tasks and notifications, frontend with updated UI components, and shared configuration for Kafka and Dapr.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Additional services | Required for proper event-driven architecture with Dapr | Would create tight coupling without separation |
| Kafka integration | Required for scalable, asynchronous processing | Direct calls would create blocking operations |
| Dapr integration | Required for proper distributed runtime | Manual service coordination would be complex |

## Phase 0: Research

### 0.1 Technology Research

**Decision**: Use confluent-kafka for Python Kafka integration
**Rationale**: Industry standard for high-performance Kafka clients in Python, well-maintained by Confluent
**Alternatives considered**: kafka-python (slower performance), aiokafka (async only)

**Decision**: Use official Dapr Python SDK
**Rationale**: Officially supported, actively maintained, provides full feature access
**Alternatives considered**: Raw HTTP API calls to Dapr sidecar (less convenient)

**Decision**: Use pgvector extension for PostgreSQL for advanced search capabilities
**Rationale**: Provides vector search alongside traditional SQL search for better performance
**Alternatives considered**: Elasticsearch (adds infrastructure complexity)

### 0.2 Architecture Research

**Decision**: Implement Recurring Task Service as a separate Dapr-enabled microservice
**Rationale**: Keeps business logic separated, enables independent scaling, follows event-driven patterns
**Alternatives considered**: Cron jobs in main API (less resilient, harder to scale)

**Decision**: Implement Notification Service as a separate Dapr-enabled microservice
**Rationale**: Handles time-sensitive operations independently, enables multiple notification types
**Alternatives considered**: In-app notifications only (limited reach, less flexible)

### 0.3 Database Schema Research

**Decision**: Use JSONB column for recurring_rule to store complex recurrence patterns
**Rationale**: Flexible schema, allows complex recurrence patterns, efficient querying
**Alternatives considered**: Separate recurrence table (more complex joins), multiple columns (rigid)

**Decision**: Use ARRAY column for tags with GIN indexing for efficient searching
**Rationale**: Native PostgreSQL support, efficient array operations and indexing
**Alternatives considered**: Separate task_tags junction table (more complex queries)

## Phase 1: Design Artifacts

### 1.1 Data Model Design

The data model will extend the existing Task model with additional fields to support advanced features:

**Task Model Extensions:**
- `priority`: ENUM('low', 'medium', 'high', 'urgent') with default 'medium'
- `tags`: TEXT[] (array of text) with GIN index for efficient searching
- `due_date`: TIMESTAMP WITH TIME ZONE nullable
- `recurrence_rule`: JSONB nullable (stores recurrence pattern as JSON)
- `completed_at`: TIMESTAMP WITH TIME ZONE nullable (for tracking completion time)
- `created_by_user_id`: UUID foreign key to user table (existing)

**New Supporting Models:**
- `RecurringTaskInstance`: Links recurring task patterns to actual instances
- `Reminder`: Stores scheduled reminder information linked to tasks
- `TaskEventLog`: Audit trail for all task operations (optional, depending on requirements)

### 1.2 API Contract Design

The API will include new endpoints and parameter support for the advanced features:

**GET /api/tasks** (extended)
- Query parameters: `search`, `priority`, `tag`, `due_date_from`, `due_date_to`, `sort`, `order`
- Response: Enhanced with priority, tags, due_date, recurrence information

**POST /api/tasks** (extended)
- Request body: Include priority, tags[], due_date, recurrence_rule
- Response: Full task object with all new fields

**Additional Endpoints:**
- `GET /api/tasks/search?q={query}` - Dedicated search endpoint
- `GET /api/tasks/filter` - Advanced filtering with multiple criteria
- `POST /api/tasks/{id}/complete` - Complete task with potential recurring instance creation
- `PUT /api/tasks/{id}/reminder` - Set/modify reminder for a task

### 1.3 Service Architecture

**Main API Service (FastAPI)**:
- Handles all CRUD operations
- Publishes events to Kafka
- Authenticates and authorizes requests
- Validates input and manages database transactions

**Recurring Task Service (Dapr-enabled)**:
- Subscribes to task completion events
- Creates new task instances based on recurrence rules
- Uses Dapr state management for tracking task instances
- Runs as separate, independently scalable service

**Notification Service (Dapr-enabled)**:
- Subscribes to reminder events
- Sends notifications based on user preferences
- Uses Dapr bindings for scheduling and delivery
- Tracks notification delivery status

## Phase 2: Implementation Preparation

### 2.1 Infrastructure Setup

**Kafka Topics Setup:**
- `task-events`: For all task lifecycle events
- `reminders`: For scheduled reminder notifications
- `task-updates`: For real-time sync notifications (bonus)

**Dapr Components:**
- `pubsub.kafka`: Kafka pub/sub component
- `state.postgres`: PostgreSQL state store
- `secrets.local`: Local secrets store for development

### 2.2 Development Workflow

**Phase 1A**: Database schema updates and basic model extensions
**Phase 1B**: API endpoint extensions with search, filter, sort
**Phase 1C**: Frontend UI updates for new fields
**Phase 2A**: Kafka integration and event publishing
**Phase 2B**: Recurring Task Service implementation
**Phase 2C**: Notification Service implementation
**Phase 3A**: MCP tool updates for chatbot integration
**Phase 3B**: End-to-end testing and integration validation

### 2.3 Quality Assurance Plan

- Unit tests for all new services and functions (>80% coverage)
- Integration tests for Kafka and Dapr components
- End-to-end tests for complete user flows
- Security tests for user isolation and data protection
- Performance tests for search and filter operations

### 2.4 Success Criteria Validation

Each feature will be validated against the success criteria from the specification:
- Recurring tasks generate new instances within 5 seconds
- Reminder notifications delivered within 1 minute
- Search queries return results within 500ms
- All features accessible through the Todo Chatbot interface
- Zero critical bugs found during testing
- End-to-end demo scenario works completely