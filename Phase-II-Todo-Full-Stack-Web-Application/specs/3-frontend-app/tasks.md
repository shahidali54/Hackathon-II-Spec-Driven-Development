---
description: "Task list for Frontend Web Application implementation"
---

# Tasks: Frontend Web Application

**Input**: Design documents from `/specs/3-frontend-app/`
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

- [X] T001 Create project structure with Next.js 16+ App Router in frontend/
- [X] T002 [P] Install Better Auth dependencies in frontend/
- [X] T003 [P] Configure Tailwind CSS for styling in frontend/
- [X] T004 Setup initial Next.js configuration files in frontend/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create API client utility in frontend/src/lib/api.ts
- [X] T006 [P] Create authentication utilities in frontend/src/lib/auth.ts
- [X] T007 [P] Create ProtectedRoute component in frontend/src/components/ProtectedRoute.tsx
- [X] T008 Create AuthGuard component in frontend/src/components/AuthGuard.tsx
- [X] T009 Setup environment variables for API communication
- [X] T010 Create context providers for global state management
- [X] T011 Configure JWT token handling in API client
- [X] T012 Implement 401 redirect to login in API client
- [X] T013 Create shared types in frontend/src/lib/types/index.ts

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Authentication (Priority: P1) 🎯 MVP

**Goal**: Enable users to sign up for the todo application and access their dashboard.

**Independent Test**: Can be fully tested by registering a new user, signing in, and verifying the user is redirected to the dashboard.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

- [ ] T014 [P] [US1] Unit tests for authentication utilities in frontend/tests/unit/auth.test.ts
- [ ] T015 [P] [US1] Integration test for auth flow in frontend/tests/integration/auth.test.ts

### Implementation for User Story 1

- [X] T016 [P] [US1] Create signup page in frontend/src/app/auth/signup/page.tsx
- [X] T017 [P] [US1] Create signin page in frontend/src/app/auth/signin/page.tsx
- [X] T018 [US1] Implement signup form with validation in frontend/src/components/SignupForm.tsx
- [X] T019 [US1] Implement signin form with validation in frontend/src/components/SigninForm.tsx
- [X] T020 [US1] Add Better Auth integration to signup page
- [X] T021 [US1] Add Better Auth integration to signin page
- [X] T022 [US1] Implement login success redirect to dashboard
- [X] T023 [US1] Implement logout functionality
- [X] T024 [US1] Handle session persistence with JWT tokens

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Management (Priority: P1)

**Goal**: Allow an authenticated user to manage their tasks through the frontend application.

**Independent Test**: Can be fully tested by authenticating a user and performing all CRUD operations on tasks.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T025 [P] [US2] Unit tests for task components in frontend/tests/unit/tasks.test.ts
- [ ] T026 [P] [US2] Integration test for task management flow in frontend/tests/integration/tasks.test.ts

### Implementation for User Story 2

- [X] T027 [P] [US2] Create dashboard page in frontend/src/app/dashboard/page.tsx
- [X] T028 [P] [US2] Create TaskList component in frontend/src/components/TaskList.tsx
- [X] T029 [P] [US2] Create TaskCard component in frontend/src/components/TaskCard.tsx
- [X] T030 [P] [US2] Create TaskForm component in frontend/src/components/TaskForm.tsx
- [X] T031 [US2] Implement task creation functionality
- [X] T032 [US2] Implement task listing with API integration
- [X] T033 [US2] Implement task editing functionality
- [X] T034 [US2] Implement task deletion functionality
- [X] T035 [US2] Add loading states during API operations
- [X] T036 [US2] Add error handling for task operations

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Task Completion Toggle (Priority: P2)

**Goal**: Allow an authenticated user to mark tasks as complete or incomplete.

**Independent Test**: Can be fully tested by authenticating a user, creating tasks, and toggling their completion status.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T037 [P] [US3] Unit tests for completion toggle functionality in frontend/tests/unit/completion.test.ts
- [ ] T038 [P] [US3] Integration test for completion flow in frontend/tests/integration/completion.test.ts

### Implementation for User Story 3

- [X] T039 [P] [US3] Add completion toggle button to TaskCard component
- [X] T040 [US3] Implement completion toggle API call
- [X] T041 [US3] Update task display to show completion status visually
- [X] T042 [P] [US3] Create task detail view in frontend/src/app/tasks/[id]/page.tsx
- [X] T043 [US3] Add completion toggle to task detail page
- [X] T044 [US3] Update TaskList to reflect completion status changes

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T045 [P] Update documentation in docs/
- [X] T046 Make UI responsive on mobile and desktop
- [X] T047 Add empty states for task lists
- [X] T048 [P] Add comprehensive error handling and messages
- [X] T049 Security hardening for frontend
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
Task: "Unit tests for authentication utilities in frontend/tests/unit/auth.test.ts"
Task: "Integration test for auth flow in frontend/tests/integration/auth.test.ts"

# Launch all components for User Story 1 together:
Task: "Create signup page in frontend/src/app/auth/signup/page.tsx"
Task: "Create signin page in frontend/src/app/auth/signin/page.tsx"
Task: "Create signup form with validation in frontend/src/components/SignupForm.tsx"
Task: "Create signin form with validation in frontend/src/components/SigninForm.tsx"
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