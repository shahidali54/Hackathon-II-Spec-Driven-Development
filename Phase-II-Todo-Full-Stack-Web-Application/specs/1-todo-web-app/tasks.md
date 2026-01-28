---
description: "Task list for Todo Full-Stack Web Application implementation"
---

# Tasks: Todo Full-Stack Web Application

**Input**: Design documents from `/specs/1-todo-web-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure with backend/ and frontend/ directories
- [X] T002 [P] Initialize Python project with FastAPI and SQLModel dependencies in backend/
- [X] T003 [P] Initialize Next.js 16+ project with App Router in frontend/
- [X] T004 [P] Configure linting and formatting tools for both backend and frontend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Setup database schema and migrations framework with Neon PostgreSQL
- [X] T006 [P] Implement JWT-based authentication/authorization framework with Better Auth
- [X] T007 [P] Setup RESTful API routing and middleware structure with FastAPI
- [X] T008 Create base models/entities that all stories depend on using SQLModel
- [X] T009 Configure error handling and logging infrastructure with proper HTTP status codes
- [X] T010 Setup environment configuration management with BETTER_AUTH_SECRET
- [X] T011 Implement user ownership verification for all task operations
- [X] T012 Create middleware to verify JWT tokens and extract user identity
- [X] T013 Implement database query filtering by authenticated user

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to sign up for the todo application and securely manage their tasks.

**Independent Test**: Can be fully tested by registering a new user, signing in, and verifying the JWT token is issued and can be used for subsequent API calls.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T014 [P] [US1] Contract test for authentication endpoints in backend/tests/contract/test_auth.py
- [ ] T015 [P] [US1] Integration test for user registration flow in backend/tests/integration/test_auth.py

### Implementation for User Story 1

- [X] T016 [P] [US1] Create User model in backend/src/models/user.py
- [X] T017 [P] [US1] Create authentication service in backend/src/services/auth_service.py
- [X] T018 [US1] Implement authentication API endpoints in backend/src/api/auth.py
- [X] T019 [US1] Add user registration and login validation and error handling
- [X] T020 [US1] Add authentication logging for user story 1 operations
- [X] T021 [P] [US1] Create authentication components in frontend/src/components/auth.tsx
- [X] T022 [US1] Implement signup page in frontend/src/app/auth/signup/page.tsx
- [X] T023 [US1] Implement signin page in frontend/src/app/auth/signin/page.tsx
- [X] T024 [US1] Integrate Better Auth with Next.js frontend

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Management (Priority: P1)

**Goal**: Allow an authenticated user to create, view, update, and delete their personal tasks.

**Independent Test**: Can be fully tested by authenticating a user and performing all CRUD operations on tasks, ensuring only that user's tasks are accessible.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T025 [P] [US2] Contract test for tasks endpoints in backend/tests/contract/test_tasks.py
- [ ] T026 [P] [US2] Integration test for task management flow in backend/tests/integration/test_tasks.py

### Implementation for User Story 2

- [X] T027 [P] [US2] Create Task model in backend/src/models/task.py
- [X] T028 [P] [US2] Create task service in backend/src/services/task_service.py
- [X] T029 [US2] Implement tasks API endpoints in backend/src/api/tasks.py
- [X] T030 [US2] Add task validation and error handling
- [X] T031 [US2] Add task logging for user story 2 operations
- [X] T032 [P] [US2] Create TaskForm component in frontend/src/components/TaskForm.tsx
- [X] T033 [P] [US2] Create TaskList component in frontend/src/components/TaskList.tsx
- [X] T034 [US2] Implement tasks page in frontend/src/app/tasks/page.tsx
- [X] T035 [US2] Connect frontend to backend API for task operations
- [X] T036 [US2] Add JWT token attachment to all task API requests

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Completion Toggle (Priority: P2)

**Goal**: Allow an authenticated user to mark tasks as complete or incomplete.

**Independent Test**: Can be fully tested by authenticating a user, creating tasks, and toggling their completion status.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T037 [P] [US3] Contract test for task completion endpoint in backend/tests/contract/test_task_completion.py
- [ ] T038 [P] [US3] Integration test for task completion flow in backend/tests/integration/test_task_completion.py

### Implementation for User Story 3

- [X] T039 [P] [US3] Extend task service with completion toggle functionality in backend/src/services/task_service.py
- [X] T040 [US3] Implement task completion API endpoint in backend/src/api/tasks.py
- [X] T041 [US3] Add completion toggle validation and error handling
- [X] T042 [P] [US3] Create task completion UI components in frontend/src/components/TaskCompletion.tsx
- [X] T043 [US3] Update task list UI to show completion status visually in frontend/src/components/TaskList.tsx
- [X] T044 [US3] Connect completion toggle to backend API in frontend

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T045 [P] Update documentation in docs/
- [X] T046 Code cleanup and refactoring
- [X] T047 Performance optimization across all stories
- [X] T048 [P] Additional unit tests in backend/tests/unit/ and frontend/tests/
- [X] T049 Security hardening
- [X] T050 Run quickstart.md validation

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

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

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Contract test for authentication endpoints in backend/tests/contract/test_auth.py"
Task: "Integration test for user registration flow in backend/tests/integration/test_auth.py"

# Launch all models for User Story 1 together:
Task: "Create User model in backend/src/models/user.py"
Task: "Create authentication service in backend/src/services/auth_service.py"
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
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence