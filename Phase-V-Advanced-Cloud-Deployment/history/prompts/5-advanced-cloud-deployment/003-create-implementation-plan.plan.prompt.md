---
id: 003
title: Create Implementation Plan
stage: plan
date: 2026-02-09
surface: agent
model: claude-opus-4-6
feature: 5-advanced-cloud-deployment
branch: 5-advanced-cloud-deployment
user: user
command: sp.plan
labels: [plan, phase-v, advanced-features, kafka, dapr, architecture]
links:
  spec: specs/5-advanced-cloud-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/5-advanced-cloud-deployment/plan.md
 - specs/5-advanced-cloud-deployment/research.md
 - specs/5-advanced-cloud-deployment/data-model.md
 - specs/5-advanced-cloud-deployment/quickstart.md
 - specs/5-advanced-cloud-deployment/contracts/task-api-openapi.yaml
tests:
 - none
---

## Prompt

```
Project: Implementation of Advanced & Intermediate Features for AI-Powered Todo Chatbot (Phase V - Part A)

Overall Goal: Follow spec-driven development to implement all required features, integrate Kafka for event-driven architecture, and Dapr for distributed runtime, building on the existing codebase from previous phases.

Step-by-Step Plan:

1. **Preparation and Setup**
   - Review existing codebase from Phases I-IV: Analyze FastAPI endpoints, SQLModel schemas, Next.js frontend components, and MCP tools integration.
   - Set up development environment: Ensure Kafka (Redpanda Cloud) credentials are configured, install Dapr CLI and SDKs (Python for backend), create necessary Kafka topics ("task-events", "reminders", "task-updates" if including sync).
   - Update dependencies: Add Kafka client (e.g., confluent-kafka or kafka-python), Dapr SDK (dapr-sdk for Python), and any required libraries for cron bindings or state management.
   - Design database schema extensions: Add fields to Task model (e.g., priority: Enum/Integer, tags: Array[String], due_date: DateTime, recurring_rule: String/JSON for interval like 'daily', 'weekly').
   - Document initial architecture diagram: Update README with high-level event flows (e.g., using ASCII art or Mermaid for producers/consumers).

2. **Implement Intermediate Features (Priorities, Tags, Search, Filter, Sort)**
   - Backend: Update SQLModel Task model with new fields. Modify CRUD endpoints in FastAPI to handle priorities, tags.
   - Add query parameters for search (full-text on title/description), filter (by priority, tags, due_date), sort (by priority, due_date).
   - Use SQLModel/SQLAlchemy for efficient querying (e.g., ilike for search, array_contains for tags).
   - Frontend: Update Next.js task creation/edit forms to include dropdown for priority, multi-select for tags, date picker for due_date.
   - Add UI components for search bar, filters (dropdowns/checkboxes), and sorting options. Ensure list view reflects filtered/sorted results via API calls.
   - Integrate with Chatbot: Update MCP tools to parse and handle new fields in natural language (e.g., "high priority", "tag:work", "due tomorrow").

3. **Implement Advanced Features (Recurring Tasks, Due Dates & Reminders)**
   - Recurring Tasks: Add logic to parse recurring_rule (e.g., using dateutil.rrule for generating next dates).
   - When task completed, publish event to "task-events"; create a separate Recurring Task Service (Dapr-enabled) that consumes and creates next instance.
   - Due Dates & Reminders: On task create/update with due_date, calculate remind_at (e.g., 1 hour before) and publish to "reminders" topic.
   - Create Notification Service (Dapr-enabled) that consumes "reminders", checks time (use Dapr cron binding for scheduling), and sends push/email (simulate with logs or integrate simple notifier).
   - Ensure services are decoupled: Chat API only publishes events, no direct calls.

Dependencies: Redpanda Cloud account, Dapr installed globally.

Success Check: Run demo script showing all features; no crashes on event flows; features map 100% to spec.
```

## Response snapshot

Created a comprehensive implementation plan for Phase V Advanced & Intermediate Features for AI-Powered Todo Chatbot. The plan includes:
- Technical context with technology stack and constraints
- Constitution check ensuring compliance with project principles
- Detailed project structure with multi-service architecture
- Phase 0 research document covering technology and architecture decisions
- Data model extending the Task entity with priority, tags, due_date, recurrence_rule fields
- Quickstart guide with setup instructions and development workflow
- API contract specification in OpenAPI format for the enhanced task API

## Outcome

- ✅ Impact: Complete implementation plan created with all required artifacts
- 🧪 Tests: none
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and contracts/task-api-openapi.yaml
- 🔁 Next prompts: Ready for task generation with /sp.tasks
- 🧠 Reflection: Plan comprehensively covers all aspects of the advanced features implementation

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation by generating tasks