---
id: 002
title: Update Phase 5 Spec with Kafka Dapr
stage: spec
date: 2026-02-09
surface: agent
model: claude-opus-4-6
feature: 5-advanced-cloud-deployment
branch: 5-advanced-cloud-deployment
user: user
command: sp.specify
labels: [spec, phase-v, advanced-features, kafka, dapr, recurring-tasks, due-dates, reminders, priorities, tags, search, filter, sort]
links:
  spec: specs/5-advanced-cloud-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/5-advanced-cloud-deployment/spec.md
tests:
 - none
---

## Prompt

```
Project: Implementation of Advanced & Intermediate Features for AI-Powered Todo Chatbot (Phase V - Part A)

Target audience: Hackathon judges and technical reviewers evaluating feature completeness, architecture quality, and event-driven design

Focus:
- Fully implement all Advanced Level features: Recurring Tasks, Due Dates & Reminders
- Fully implement all Intermediate Level features: Priorities, Tags, Search, Filter, Sort
- Introduce event-driven architecture using Kafka (Redpanda Cloud)
- Integrate Dapr as the distributed application runtime for services

Success criteria:
- All listed features are completely working in the existing FastAPI + Next.js application
- Recurring tasks automatically create the next occurrence when marked complete
- Due-date based reminders are scheduled and triggered correctly (via Kafka events)
- Priorities, Tags, Search, Filter, Sort are fully functional in both API and frontend
- Kafka is used for at least these flows:
  - Publishing task CRUD events ("task-events" topic)
  - Publishing reminder triggers ("reminders" topic)
  - Publishing task completion for recurring logic
  - (Bonus) Publishing updates for real-time sync ("task-updates" topic)
- Dapr is integrated and used for:
  - Pub/Sub (Kafka component)
  - State management
  - Service Invocation between services
  - Secrets management
  - Bindings (especially cron for reminder checks if needed)
- All new features are accessible and usable through the Todo Chatbot interface (MCP tools)
- Backend and frontend both reflect the new fields and behaviors
- Basic end-to-end tests or manual verification scenarios exist for each major feature
- Code follows clean architecture, proper error handling, and input validation

Constraints:
- Build on existing Phase II–IV codebase (Next.js, FastAPI, SQLModel, Neon DB)
- Use Kafka via Redpanda Cloud (managed Kafka)
- Use official Dapr SDKs (Python for FastAPI services, JS if needed for frontend-related parts)
- Do NOT change the core database schema drastically unless absolutely required (prefer additive changes)
- Do NOT implement full cloud deployment yet (Minikube/DOKS deployment is out of scope in this spec)
- Do NOT implement WebSocket real-time sync OR full audit service unless time permits (focus on core 4 use-cases first)
- Keep frontend changes minimal but functional (add necessary UI controls for priority, tags, due dates, recurring options)

Not building in this part:
- Local Minikube deployment with Dapr
- DigitalOcean Kubernetes (DOKS) deployment
- Full CI/CD pipeline
- Complete monitoring/logging setup
- Advanced audit log UI
- Full real-time multi-client WebSocket sync (only event publishing for now)

Timeline goal: Complete and stable implementation of all listed features before moving to deployment phases

Deliverables expected:
- Updated database schema (new fields: priority, tags, due_date, recurring_rule/interval/etc.)
- Updated FastAPI endpoints and SQLModel models
- New Kafka producer logic in Chat API / MCP tools
- At least 2–3 new Dapr-enabled services or components (e.g. Recurring Task Service, Notification/Reminder Service)
- Dapr pub/sub configuration for Kafka
- Updated Next.js frontend to support new task fields and display them properly
- README section explaining the new features + event flows
- Basic demonstration script or test cases showing the features working
```

## Response snapshot

Updated the Phase 5 specification to include detailed requirements for Advanced & Intermediate features with Kafka and Dapr integration. The spec now includes comprehensive user stories, functional requirements, success criteria, and key entities for implementing recurring tasks, due dates & reminders, priorities, tags, search, filter, and sort functionality with event-driven architecture and distributed runtime components.

## Outcome

- ✅ Impact: Enhanced Phase 5 spec with detailed Kafka/Dapr integration requirements and advanced features
- 🧪 Tests: none
- 📁 Files: Updated specs/5-advanced-cloud-deployment/spec.md with comprehensive requirements
- 🔁 Next prompts: Proceed with creating plan and tasks for Phase 5 implementation
- 🧠 Reflection: Successfully incorporated all advanced features and technology requirements into the spec

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation planning for Phase 5 features with Kafka and Dapr