# Phase V Advanced Features Documentation

## Overview

Phase V adds enterprise-grade advanced features to the Todo application, including:
- **Recurring Tasks**: Automated task creation based on schedules
- **Due Dates & Reminders**: Scheduling and notification system
- **Task Priorities**: Four-level priority system with visual indicators
- **Tags**: Flexible task categorization and organization
- **Advanced Search & Filter**: Full-text search and multi-criteria filtering
- **Event-Driven Architecture**: Kafka integration for asynchronous operations
- **Distributed Runtime**: Dapr integration for microservices communication

## Quick Start

### Backend Setup

1. **Install Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Configure Environment Variables**
   Create a `.env` file in the backend directory:
   ```
   DATABASE_URL=postgresql://user:password@localhost/todo_db
   OPENAI_API_KEY=your-api-key-here
   JWT_SECRET_KEY=your-secret-key-here
   KAFKA_BOOTSTRAP_SERVERS=localhost:9092
   DAPR_HOST=localhost
   DAPR_HTTP_PORT=3500
   DAPR_GRPC_PORT=50001
   ```

3. **Initialize Database**
   ```bash
   python init_db.py
   ```

4. **Start the Main API**
   ```bash
   python -m uvicorn src.main:app --reload --port 8000
   ```

### Frontend Setup

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure Environment Variables**
   Create a `.env.local` file:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Start the Frontend**
   ```bash
   npm run dev
   ```

### Standalone Services

1. **Recurring Task Service**
   ```bash
   cd services/recurring-task-service
   pip install -r requirements.txt
   python app.py
   ```

2. **Notification Service**
   ```bash
   cd services/notification-service
   pip install -r requirements.txt
   python app.py
   ```

## Feature Details

### 1. Recurring Tasks

#### Create a Recurring Task

**Request:**
```bash
POST /api/tasks
Content-Type: application/json

{
  "title": "Weekly Team Meeting",
  "description": "Team sync meeting every Monday",
  "priority": "high",
  "due_date": "2026-02-17T10:00:00",
  "recurrence_rule": {
    "enabled": true,
    "frequency": "weekly",
    "interval": 1
  }
}
```

**Response:**
```json
{
  "id": "uuid-string",
  "title": "Weekly Team Meeting",
  "description": "Team sync meeting every Monday",
  "priority": "high",
  "due_date": "2026-02-17T10:00:00",
  "recurrence_rule": {
    "enabled": true,
    "frequency": "weekly",
    "interval": 1
  },
  "is_completed": false,
  "created_at": "2026-02-09T14:00:00",
  "updated_at": "2026-02-09T14:00:00"
}
```

#### Supported Frequencies
- `daily` - Task repeats every N days
- `weekly` - Task repeats every N weeks
- `monthly` - Task repeats every N months
- `yearly` - Task repeats every N years

#### How It Works
1. User creates a task with `recurrence_rule.enabled: true`
2. When the task is marked as completed, a `task_completion_toggled` event is published to Kafka
3. The Recurring Task Service receives the event and:
   - Verifies the task has a recurrence rule
   - Calculates the next occurrence date
   - Creates a new task instance automatically
4. The new task appears in the user's task list

### 2. Due Dates & Reminders

#### Set a Due Date and Reminder

**Request:**
```bash
POST /api/tasks
{
  "title": "Project Deadline",
  "due_date": "2026-02-28T18:00:00",
  "priority": "urgent"
}
```

**Create a Reminder:**
```bash
POST /api/tasks/{task_id}/reminders?remind_at=2026-02-27T09:00:00
```

#### Get Upcoming Reminders

```bash
GET /api/reminders/upcoming

Response:
[
  {
    "id": "reminder-uuid",
    "task_id": "task-uuid",
    "remind_at": "2026-02-27T09:00:00"
  }
]
```

#### Visual Indicators in UI
- **Overdue Tasks**: Red badge with ⚠️ icon
- **Due Within 24 Hours**: Yellow badge with 📅 icon
- **Normal Due Date**: Gray badge

### 3. Task Priorities

#### Priority Levels

| Priority | Color | Use Case |
|----------|-------|----------|
| Low | Green | Nice-to-have tasks, no urgency |
| Medium | Yellow | Regular tasks with normal urgency |
| High | Orange | Important tasks that need attention |
| Urgent | Red | Critical tasks that must be done ASAP |

#### Filter by Priority

```bash
GET /api/tasks?priority=high

GET /api/tasks/filter?priority=urgent&sort=due_date&order=asc
```

#### Sort by Priority

```bash
GET /api/tasks?sort=priority&order=desc
```

### 4. Tags

#### Add Tags to a Task

**Request:**
```bash
POST /api/tasks
{
  "title": "Design new landing page",
  "tags": ["design", "frontend", "high-priority"]
}
```

#### Search and Filter by Tags

```bash
# Filter by single tag
GET /api/tasks?tags=frontend

# Filter by multiple tags
GET /api/tasks/filter?tags=design,frontend

# Search + Filter
GET /api/tasks/search?q=landing&tags=design
```

#### Tag Management
- Tags are stored as an array of strings
- Case-sensitive matching
- No predefined tag list - users create tags organically
- Fast filtering using PostgreSQL array operators

### 5. Advanced Search & Filter

#### Full-Text Search

```bash
GET /api/tasks/search?q=project%20deadline&limit=50
```

Searches across:
- Task titles
- Task descriptions
- Returns matching tasks with highlighted results (frontend responsibility)

#### Advanced Filtering

```bash
# Complex filter example
GET /api/tasks/filter?
  priority=high
  &tags=urgent,important
  &completed=false
  &due_date_from=2026-02-01
  &due_date_to=2026-02-28
  &sort=due_date
  &order=asc
  &limit=20
  &offset=0
```

**Query Parameters:**
- `priority` - Filter by priority level
- `tags` - Comma-separated tag list
- `completed` - Filter by completion status (true/false)
- `due_date_from` - Start date for due date range
- `due_date_to` - End date for due date range
- `search` - Full-text search query
- `sort` - Field to sort by (title, due_date, priority, created_at)
- `order` - Sort order (asc/desc)
- `limit` - Results per page (1-100)
- `offset` - Pagination offset

## Event-Driven Architecture

### Kafka Topics

#### task-events
Published by: Main API
Consumed by: Recurring Task Service

**Events:**
- `task_created` - Task was created
- `task_updated` - Task was updated
- `task_deleted` - Task was deleted
- `task_completion_toggled` - Task completion status changed
- `recurring_task_generated` - New recurring task instance created

**Sample Event:**
```json
{
  "event_type": "task_completion_toggled",
  "task_id": "task-uuid",
  "user_id": "user-uuid",
  "timestamp": "2026-02-09T14:30:00Z",
  "payload": {
    "is_completed": true,
    "title": "Weekly Meeting",
    "has_recurrence": true
  }
}
```

#### reminders
Published by: Main API / Reminder Service
Consumed by: Notification Service

**Events:**
- `reminder_triggered` - Reminder time reached

**Sample Event:**
```json
{
  "event_type": "reminder_triggered",
  "task_id": "task-uuid",
  "user_id": "user-uuid",
  "reminder_time": "2026-02-09T09:00:00Z",
  "timestamp": "2026-02-09T09:00:01Z"
}
```

#### task-updates
Published by: Task Service
Used for: Real-time client updates (future use)

### Event Flow Diagram

```
User Creates Recurring Task
            ↓
    Main API (POST /tasks)
            ↓
    Task saved to database
            ↓
    Publish: task_created event
            ↓
        (Kafka Topic: task-events)
            ↓
    User marks task complete
            ↓
    Publish: task_completion_toggled
            ↓
        (Kafka Topic: task-events)
            ↓
    Recurring Task Service
            ↓
    Check for recurrence rule
            ↓
    Call Main API to create next task
            ↓
    New task instance created
```

## Dapr Integration

### Current Implementation

The application includes Dapr configuration files in `backend/dapr/components/`:

1. **pubsub.yaml** - Kafka pub/sub configuration
2. **statestore.yaml** - PostgreSQL state store
3. **secrets.yaml** - Secrets management
4. **bindings.cron.yaml** - Cron job bindings

### DaprClientService

Provides utilities for Dapr operations:

```python
from src.services.dapr_client import DaprClientService

# Publish an event
DaprClientService.publish_event(
    pubsub_name='kafka-pubsub',
    topic_name='task-events',
    data={'event_type': 'task_created', 'task_id': '...'}
)

# Invoke another service
response = DaprClientService.invoke_service(
    method='POST',
    service_url='http://localhost:8000/api/tasks',
    data={'title': 'New Task'}
)

# State management
DaprClientService.save_state(
    store_name='postgresql-state-store',
    key='user-123:preferences',
    value={'theme': 'dark'}
)
```

### Standalone Services

**Recurring Task Service** (Port 8001)
- Listens to `task-events` topic
- Creates next occurrence for recurring tasks
- Health check: `GET http://localhost:8001/health`

**Notification Service** (Port 8002)
- Listens to `reminders` topic
- Sends reminder notifications (currently logs)
- Health check: `GET http://localhost:8002/health`
- Metrics: `GET http://localhost:8002/metrics`

## API Reference

### Task Endpoints

#### Create Task
```
POST /api/tasks
Authorization: Bearer {token}
Content-Type: application/json

{
  "title": "Task title",
  "description": "Optional description",
  "due_date": "2026-02-28T18:00:00",
  "priority": "high",
  "tags": ["tag1", "tag2"],
  "recurrence_rule": {
    "enabled": false,
    "frequency": "daily",
    "interval": 1
  }
}
```

#### Get Tasks with Filters
```
GET /api/tasks?
  priority=high
  &tags=work
  &completed=false
  &sort=due_date
  &order=asc
  &limit=50
```

#### Search Tasks
```
GET /api/tasks/search?q=project+meeting
```

#### Filter Tasks
```
GET /api/tasks/filter?
  priority=urgent
  &tags=important
  &due_date_from=2026-02-01
  &due_date_to=2026-02-28
```

#### Update Task
```
PUT /api/tasks/{task_id}
{
  "title": "Updated title",
  "priority": "medium",
  "tags": ["updated-tag"]
}
```

#### Toggle Completion
```
PATCH /api/tasks/{task_id}/complete?completed=true
```

#### Delete Task
```
DELETE /api/tasks/{task_id}
```

### Reminder Endpoints

#### Create Reminder
```
POST /api/tasks/{task_id}/reminders?remind_at=2026-02-27T09:00:00
```

#### Get Task Reminders
```
GET /api/tasks/{task_id}/reminders
```

#### Get Upcoming Reminders
```
GET /api/reminders/upcoming
```

#### Delete Reminder
```
DELETE /api/reminders/{reminder_id}
```

## Frontend Components

### TaskForm Component

Enhanced with all advanced features:
- Priority selector (Low, Medium, High, Urgent)
- Due date picker (datetime input)
- Tag input with add/remove buttons
- Recurrence pattern configuration
  - Enable/disable toggle
  - Frequency selector (daily, weekly, monthly, yearly)
  - Interval input (number)

### TaskCard Component

Displays:
- Task title and description
- Priority badge with color coding
- Due date with visual urgency indicators
- Tag pills with # prefix
- Recurring indicator (🔄)
- Timestamps
- Edit/delete buttons

### TaskFilter Component

Advanced filtering UI:
- Completion status tabs (All, Active, Completed)
- Expandable advanced filters section
- Priority filter buttons
- Tag filter buttons
- Sort options (due date, priority, etc.)

## Testing the Features

### Manual Test Scenario

1. **Create Recurring Task**
   - Title: "Daily Standup"
   - Time: 10:00 AM daily
   - Priority: High
   - Tags: work, meeting

2. **Mark as Complete**
   - Watch as new task is created for next day
   - Check event in Kafka logs

3. **Add Reminder**
   - Set reminder for 30 min before due date
   - Notification service logs reminder send

4. **Filter and Search**
   - Search: "standup"
   - Filter by: Tag=work, Priority=high
   - Sort by: due_date ascending

5. **Test Overdue**
   - Create task with past due date
   - See red overdue indicator

## Monitoring & Debugging

### Kafka Topics Monitoring

```bash
# List topics
kafka-topics.sh --list --bootstrap-server localhost:9092

# Monitor topic messages
kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic task-events \
  --from-beginning
```

### Service Health Checks

```bash
# Main API
curl http://localhost:8000/health

# Recurring Task Service
curl http://localhost:8001/health

# Notification Service
curl http://localhost:8002/health
curl http://localhost:8002/metrics
```

### Database Queries

```sql
-- List all tasks with recurrence rules
SELECT id, title, user_id, recurrence_rule FROM "task" 
WHERE recurrence_rule IS NOT NULL 
AND recurrence_rule != '{}';

-- List pending reminders
SELECT r.id, r.task_id, r.remind_at, t.title 
FROM reminder r
JOIN "task" t ON r.task_id = t.id
WHERE r.sent = false
AND r.remind_at <= NOW();
```

## Common Issues & Solutions

### Kafka Connection Error
**Problem**: "Failed to initialize real Kafka producer"
**Solution**: Ensure Kafka is running on localhost:9092 or set `KAFKA_BOOTSTRAP_SERVERS` env var

### Missing Task Fields
**Problem**: Priority, tags not showing in API response
**Solution**: Frontend types may be out of sync - rebuild frontend and check API schema

### Recurring Task Not Generated
**Problem**: Completed task doesn't create next occurrence
**Solution**: 
1. Check Recurring Task Service is running
2. Verify Kafka topics are created
3. Check service logs for errors

### Reminder Not Sending
**Problem**: Reminders not received
**Solution**:
1. Check Notification Service is running
2. Verify reminder was created: `GET /api/reminders/upcoming`
3. Check service logs and metrics

## Performance Considerations

- **Database Indices**: Ensure indices on user_id, priority, tags, due_date
- **Kafka Batch Size**: Configure for your throughput needs
- **Pagination**: Always use limit/offset to avoid large result sets
- **Search**: Full-text search can be slow on large datasets - consider adding PostgreSQL full-text search indices

## Security Notes

- All endpoints require JWT authentication (except /auth/*)
- User data is isolated by user_id
- Reminders are user-specific only
- Kafka topics are not secured in mock mode - use SASL in production
- Dapr components should have proper security in production

## Future Enhancements

1. **WebSocket Real-time Updates**: Use Dapr service invocation for real-time sync
2. **Email Notifications**: Integrate with email service for reminders
3. **Recurring Task Templates**: Pre-built templates for common recurring tasks
4. **Analytics Dashboard**: Track task completion rates and patterns
5. **Team Collaboration**: Share tasks and reminders with team members
6. **Mobile App**: Native iOS/Android apps with offline support
7. **Advanced Recurrence**: More complex patterns (e.g., "every 2nd Tuesday")
8. **Reminders via SMS/Push**: Multiple notification channels

## Support & Contribution

For issues, questions, or contributions, please refer to the main project repository documentation.
