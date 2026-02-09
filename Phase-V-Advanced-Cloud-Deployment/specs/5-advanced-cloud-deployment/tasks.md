---
description: "Task list for implementing Advanced & Intermediate Features for AI-Powered Todo Chatbot (Phase V - Part A)"
---

# Tasks: Implementation of Advanced & Intermediate Features for AI-Powered Todo Chatbot (Phase V - Part A)

**Input**: Design documents from `/specs/5-advanced-cloud-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`, `services/`
- **Paths shown below based on plan.md structure**

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for advanced features with Kafka and Dapr

- [X] T001 Create Kafka topics configuration in .kafka/topics/task-events.json
- [X] T002 Create Kafka topics configuration in .kafka/topics/reminders.json
- [X] T003 Create Kafka topics configuration in .kafka/topics/task-updates.json
- [X] T004 [P] Set up Dapr components configuration in backend/dapr/components/pubsub.yaml
- [X] T005 [P] Set up Dapr components configuration in backend/dapr/components/statestore.yaml
- [X] T006 [P] Set up Dapr components configuration in backend/dapr/components/secrets.yaml
- [X] T007 Create Dapr configuration in backend/dapr/config.yaml
- [X] T008 Update backend requirements.txt with Kafka and Dapr dependencies
- [ ] T009 Update frontend package.json with any required dependencies for advanced features

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T010 Update Task model with new fields in backend/src/models/task.py
- [X] T011 Create RecurringTaskPattern model in backend/src/models/recurring_task_pattern.py
- [X] T012 Create Reminder model in backend/src/models/reminder.py
- [X] T013 Update Task schema with new fields in backend/src/schemas/task.py
- [X] T014 Create RecurringTaskPattern schema in backend/src/schemas/recurring_task_pattern.py
- [X] T015 Create Reminder schema in backend/src/schemas/reminder.py
- [X] T016 Update database migration files to add new columns and tables
- [X] T017 Create Kafka producer service in backend/src/services/kafka_producer.py
- [X] T018 Create Kafka consumer base service in backend/src/services/kafka_consumer.py
- [X] T019 Set up Dapr client configuration in backend/src/services/dapr_client.py
- [X] T020 Update existing task service with new functionality in backend/src/services/task_service.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Recurring Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks that repeat on a schedule (daily, weekly, monthly, yearly) and automatically generate new instances when completed

**Independent Test**: User creates a recurring task, marks it as complete, and verifies the system automatically creates the next occurrence according to the recurrence pattern

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T021 [P] [US1] Contract test for recurring task creation endpoint in backend/tests/contract/test_recurring_tasks.py
- [ ] T022 [P] [US1] Integration test for recurring task completion flow in backend/tests/integration/test_recurring_flow.py

### Implementation for User Story 1

- [X] T023 [P] [US1] Create RecurringTaskService in backend/src/services/recurring_service.py
- [X] T024 [US1] Update TaskService to handle recurrence_rule in backend/src/services/task_service.py
- [X] T025 [US1] Implement recurrence rule parsing and next occurrence calculation in backend/src/utils/recurrence.py
- [X] T026 [US1] Create endpoint for recurring task creation in backend/src/api/tasks.py
- [X] T027 [US1] Implement logic to generate next task instance on completion in backend/src/services/recurring_service.py
- [X] T028 [US1] Update Kafka producer to publish recurring task events in backend/src/services/kafka_producer.py
- [X] T029 [US1] Create recurring task service in services/recurring-task-service/app.py
- [ ] T030 [US1] Implement frontend component for recurrence options in frontend/src/components/RecurrenceOptions.jsx
- [ ] T031 [US1] Update task creation form with recurrence options in frontend/src/components/TaskForm.jsx

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Due Dates & Reminders (Priority: P1)

**Goal**: Enable users to assign due dates to tasks and receive timely reminders through event-driven architecture using Kafka

**Independent Test**: User creates a task with a due date and reminder settings, and verifies that reminder events are published to Kafka and processed appropriately

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T032 [P] [US2] Contract test for reminder creation endpoint in backend/tests/contract/test_reminders.py
- [ ] T033 [P] [US2] Integration test for reminder processing flow in backend/tests/integration/test_reminder_flow.py

### Implementation for User Story 2

- [X] T034 [P] [US2] Create ReminderService in backend/src/services/reminder_service.py
- [X] T035 [US2] Update TaskService to handle due_date and reminder logic in backend/src/services/task_service.py
- [ ] T036 [US2] Create endpoint for setting/updating reminders in backend/src/api/tasks.py
- [X] T037 [US2] Implement reminder scheduling logic in backend/src/services/reminder_service.py
- [X] T038 [US2] Update Kafka producer to publish reminder events in backend/src/services/kafka_producer.py
- [X] T039 [US2] Create notification service in services/notification-service/app.py
- [ ] T040 [US2] Implement reminder UI component in frontend/src/components/ReminderOptions.jsx
- [ ] T041 [US2] Update task form with due date and reminder options in frontend/src/components/TaskForm.jsx
- [X] T042 [US2] Create Dapr binding for reminder scheduling in backend/dapr/components/bindings.cron.yaml

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Priorities (Priority: P2)

**Goal**: Allow users to assign priority levels to tasks and have these reflected in API and frontend with appropriate sorting and visual indicators

**Independent Test**: User assigns different priority levels to tasks and verifies they are sorted correctly and visually indicated in both API responses and UI

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T043 [P] [US3] Contract test for priority filtering endpoint in backend/tests/contract/test_priority_filter.py
- [ ] T044 [P] [US3] Integration test for priority-based sorting in backend/tests/integration/test_priority_sort.py

### Implementation for User Story 3

- [X] T045 [P] [US3] Update TaskService to handle priority filtering and sorting in backend/src/services/task_service.py
- [X] T046 [US3] Create endpoint for priority-based filtering in backend/src/api/tasks.py
- [X] T047 [US3] Implement priority validation and processing in backend/src/services/task_service.py
- [ ] T048 [US3] Create PrioritySelector component in frontend/src/components/PrioritySelector.jsx
- [ ] T049 [US3] Update task list to display priority indicators in frontend/src/components/TaskList.jsx
- [ ] T050 [US3] Update task form with priority selection in frontend/src/components/TaskForm.jsx

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Task Tags (Priority: P2)

**Goal**: Allow users to categorize tasks with custom tags enabling better organization and filtering through both API and frontend

**Independent Test**: User creates custom tags, assigns them to tasks, and verifies filtering and search functionality works correctly in both API and UI

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T051 [P] [US4] Contract test for tag-based filtering endpoint in backend/tests/contract/test_tag_filter.py
- [ ] T052 [P] [US4] Integration test for tag management flow in backend/tests/integration/test_tag_flow.py

### Implementation for User Story 4

- [ ] T053 [P] [US4] Update TaskService to handle tag operations in backend/src/services/task_service.py
- [ ] T054 [US4] Create endpoint for tag-based filtering in backend/src/api/tasks.py
- [ ] T055 [US4] Implement tag validation and processing in backend/src/services/task_service.py
- [ ] T056 [US4] Create TagManager component in frontend/src/components/TagManager.jsx
- [ ] T057 [US4] Update task list to display tags in frontend/src/components/TaskList.jsx
- [ ] T058 [US4] Update task form with tag selection in frontend/src/components/TaskForm.jsx

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 7: User Story 5 - Advanced Search & Filter & Sort (Priority: P1)

**Goal**: Enable users to quickly find specific tasks using search functionality and filter by various criteria while sorting as needed

**Independent Test**: User creates various tasks with different attributes, performs searches, filters, and sorts, and verifies accurate and performant results in both API and UI

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T059 [P] [US5] Contract test for search endpoint in backend/tests/contract/test_search.py
- [ ] T060 [P] [US5] Integration test for combined search/filter/sort operations in backend/tests/integration/test_advanced_queries.py

### Implementation for User Story 5

- [X] T061 [P] [US5] Update TaskService with search and filter logic in backend/src/services/task_service.py
- [X] T062 [US5] Create dedicated search endpoint in backend/src/api/tasks.py
- [X] T063 [US5] Implement efficient search algorithms in backend/src/services/task_service.py
- [X] T064 [US5] Update database queries for optimized filtering in backend/src/services/task_service.py
- [ ] T065 [US5] Create SearchBar component in frontend/src/components/SearchBar.jsx
- [ ] T066 [US5] Update task list with search and filter UI in frontend/src/components/TaskList.jsx
- [ ] T067 [US5] Implement advanced filtering options in frontend/src/components/TaskFilters.jsx

**Checkpoint**: At this point, all user stories should be independently functional

---

## Phase 8: User Story 6 - Event-Driven Architecture with Kafka (Priority: P1)

**Goal**: Handle asynchronous operations like reminder triggering and recurring task generation through event streams using Kafka

**Independent Test**: Create tasks that trigger events, verify events are published to specific Kafka topics, and confirm consumers process them correctly

### Tests for User Story 6 (OPTIONAL - only if tests requested) ⚠️

- [ ] T068 [P] [US6] Contract test for Kafka event publishing in backend/tests/contract/test_kafka_events.py
- [ ] T069 [P] [US6] Integration test for complete event-driven flow in backend/tests/integration/test_event_flow.py

### Implementation for User Story 6

- [ ] T070 [P] [US6] Implement recurring task consumer service in services/recurring-task-service/app.py
- [ ] T071 [US6] Implement notification consumer service in services/notification-service/app.py
- [ ] T072 [US6] Create Kafka consumer configuration in services/recurring-task-service/config.py
- [ ] T073 [US6] Create Kafka consumer configuration in services/notification-service/config.py
- [ ] T074 [US6] Implement event processing logic in recurring task service
- [ ] T075 [US6] Implement event processing logic in notification service
- [ ] T076 [US6] Add Kafka health checks to services
- [ ] T077 [US6] Configure Kafka producers in backend for all event types

**Checkpoint**: At this point, all user stories should work with full event-driven architecture

---

## Phase 9: User Story 7 - Dapr Integration for Distributed Runtime (Priority: P1)

**Goal**: Leverage Dapr for service-to-service communication, state management, and secrets handling in preparation for cloud deployment

**Independent Test**: Verify Dapr components handle pub/sub messaging with Kafka, state management, service invocation, and secrets access correctly

### Tests for User Story 7 (OPTIONAL - only if tests requested) ⚠️

- [ ] T078 [P] [US7] Contract test for Dapr service invocation in backend/tests/contract/test_dapr_invocation.py
- [ ] T079 [P] [US7] Integration test for complete Dapr flow in backend/tests/integration/test_dapr_flow.py

### Implementation for User Story 7

- [ ] T080 [P] [US7] Update recurring task service to use Dapr pub/sub in services/recurring-task-service/app.py
- [ ] T081 [US7] Update notification service to use Dapr pub/sub in services/notification-service/app.py
- [ ] T082 [US7] Implement Dapr service invocation in backend for inter-service communication
- [ ] T083 [US7] Configure Dapr state management for services
- [ ] T084 [US7] Implement Dapr secrets management for sensitive data
- [ ] T085 [US7] Update all services to use Dapr for communication

**Checkpoint**: All user stories now work with complete Dapr integration

---

## Phase 10: User Story 8 - Todo Chatbot Integration (Priority: P1)

**Goal**: Ensure all new advanced features are accessible and usable through the Todo Chatbot interface using MCP tools

**Independent Test**: Use the chatbot interface to create, modify, and interact with tasks using all new features (recurring, due dates, priorities, tags, search, filter, sort)

### Tests for User Story 8 (OPTIONAL - only if tests requested) ⚠️

- [ ] T086 [P] [US8] Contract test for chatbot integration with new features in backend/tests/contract/test_chatbot_integration.py
- [ ] T087 [P] [US8] Integration test for complete chatbot flow with advanced features in backend/tests/integration/test_chatbot_flow.py

### Implementation for User Story 8

- [ ] T088 [P] [US8] Update MCP tools to handle priority field in MCP configuration
- [ ] T089 [US8] Update MCP tools to handle tags field in MCP configuration
- [ ] T090 [US8] Update MCP tools to handle due date field in MCP configuration
- [ ] T091 [US8] Update MCP tools to handle recurrence rules in MCP configuration
- [ ] T092 [US8] Create new MCP tools for search and filtering operations
- [ ] T093 [US8] Update chatbot to recognize and process new commands for advanced features

**Checkpoint**: All features now accessible through the AI chatbot interface

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T094 [P] Update README with architecture diagram and new feature explanations in README.md
- [ ] T095 [P] Add documentation for Kafka event flows in docs/kafka-event-flows.md
- [ ] T096 [P] Add documentation for Dapr component configuration in docs/dapr-configuration.md
- [ ] T097 [P] Add demo script showing all features working together in demo-script.md
- [ ] T098 [P] Performance optimization across all services
- [ ] T099 [P] Security hardening for new features
- [ ] T100 Run end-to-end validation with all features working together

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1-US3 but should be independently testable
- **User Story 5 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1-US4 but should be independently testable
- **User Story 6 (P1)**: Depends on US1-US5 being implemented, as events are generated from those features
- **User Story 7 (P1)**: Depends on US6 being implemented, as Dapr integration is applied to existing services
- **User Story 8 (P1)**: Can start after Foundational (Phase 2) but should be implemented after other stories are complete

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members
- Services can be developed in parallel with frontend components

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create RecurringTaskService in backend/src/services/recurring_service.py"
Task: "Update TaskService to handle recurrence_rule in backend/src/services/task_service.py"

# Launch frontend and backend components together:
Task: "Create recurring task service in services/recurring-task-service/app.py"
Task: "Implement frontend component for recurrence options in frontend/src/components/RecurrenceOptions.jsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Add User Story 6 → Test independently → Deploy/Demo
8. Add User Story 7 → Test independently → Deploy/Demo
9. Add User Story 8 → Test independently → Deploy/Demo
10. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Stories 1 & 2 (P1 features)
   - Developer B: User Stories 3 & 4 (P2 features)
   - Developer C: User Stories 5 & 6 (P1 features)
3. Developer D: User Stories 7 & 8 (Integration features)
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence