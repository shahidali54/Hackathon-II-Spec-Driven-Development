---
description: "Task list template for feature implementation"
---

# Tasks: In-Memory Python Console Todo App

**Input**: Design documents from `/specs/001-python-todo-cli/`
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

- [X] T001 Create project structure per implementation plan
- [X] T002 [P] Initialize pyproject.toml with Python 3.13+ requirement
- [X] T003 [P] Create src/ directory structure with __init__.py files
- [X] T004 [P] Create tests/ directory structure with __init__.py files

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Domain Layer Implementation

- [X] T005 [P] Create TodoItem dataclass in src/domain/models.py
- [X] T006 [P] Create InMemoryTodoStore repository in src/domain/repository.py
- [X] T007 [P] Create TodoService in src/application/services.py (with all CRUD operations)

### CLI Layer Foundation

- [X] T008 [P] Create CLI argument parser in src/cli/parser.py
- [X] T009 [P] Create output formatter in src/cli/formatter.py
- [X] T010 [P] Create main.py entry point with basic CLI loop structure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Todos (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new todo items and view their current todo list

**Independent Test**: Can be fully tested by running the CLI with add and list commands, and verifying todos appear in the output.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T011 [P] [US1] Unit test for TodoItem model validation in tests/unit/test_models.py
- [X] T012 [P] [US1] Unit test for add operation in tests/unit/test_repository.py
- [X] T013 [P] [US1] Unit test for list operations in tests/unit/test_repository.py

### Implementation for User Story 1

- [X] T014 [P] [US1] Implement add todo functionality in src/application/services.py
- [X] T015 [P] [US1] Implement list all todos functionality in src/application/services.py
- [X] T016 [US1] Implement add command parsing in src/cli/parser.py
- [X] T017 [US1] Implement list command parsing in src/cli/parser.py
- [X] T018 [US1] Implement add command handler in src/main.py
- [X] T019 [US1] Implement list command handler in src/main.py
- [X] T020 [US1] Implement todo list output formatting in src/cli/formatter.py
- [X] T021 [US1] Add basic help command functionality

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Mark Todos as Complete (Priority: P1)

**Goal**: Enable users to mark todo items as complete to track their progress

**Independent Test**: Can be fully tested by adding todos, marking one as complete, and verifying the list shows the correct completion status.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T022 [P] [US2] Unit test for mark complete operation in tests/unit/test_repository.py
- [X] T023 [P] [US2] Unit test for mark complete service logic in tests/unit/test_services.py

### Implementation for User Story 2

- [X] T024 [P] [US2] Implement mark complete functionality in src/application/services.py
- [X] T025 [US2] Implement complete command parsing in src/cli/parser.py
- [X] T026 [US2] Implement complete command handler in src/main.py
- [X] T027 [US2] Update todo list output formatting to show completion status in src/cli/formatter.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Existing Todos (Priority: P2)

**Goal**: Enable users to edit the text of existing todo items to correct mistakes or refine task descriptions

**Independent Test**: Can be fully tested by adding a todo, updating its text, and verifying the updated text appears in the list.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T028 [P] [US3] Unit test for update operation in tests/unit/test_repository.py
- [X] T029 [P] [US3] Unit test for update service logic in tests/unit/test_services.py

### Implementation for User Story 3

- [X] T030 [P] [US3] Implement update todo functionality in src/application/services.py
- [X] T031 [US3] Implement update command parsing in src/cli/parser.py
- [X] T032 [US3] Implement update command handler in src/main.py

**Checkpoint**: User Stories 1, 2, and 3 should now be independently functional

---

## Phase 6: User Story 4 - Delete Todos (Priority: P3)

**Goal**: Enable users to remove todo items to clean up completed or unwanted tasks

**Independent Test**: Can be fully tested by adding todos, deleting one, and verifying it no longer appears in the list.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [X] T033 [P] [US4] Unit test for delete operation in tests/unit/test_repository.py
- [X] T034 [P] [US4] Unit test for delete service logic in tests/unit/test_services.py

### Implementation for User Story 4

- [X] T035 [P] [US4] Implement delete todo functionality in src/application/services.py
- [X] T036 [US4] Implement delete command parsing in src/cli/parser.py
- [X] T037 [US4] Implement delete command handler in src/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T038 [P] Add error handling for invalid todo IDs in src/application/services.py
- [X] T039 [P] Add validation for empty todo titles in src/domain/models.py
- [X] T040 [P] Add input validation for command arguments in src/cli/parser.py
- [X] T041 [P] Add proper error message formatting in src/cli/formatter.py
- [X] T042 [P] Add comprehensive CLI help text in src/cli/parser.py
- [X] T043 [P] Add edge case handling (empty list, invalid IDs, etc.)
- [X] T044 [P] Add README.md with usage instructions
- [X] T045 [P] Add integration tests for full CLI workflows in tests/integration/test_cli.py

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
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1/US2/US3 but should be independently testable

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
Task: "Unit test for TodoItem model validation in tests/unit/test_models.py"
Task: "Unit test for add operation in tests/unit/test_repository.py"
Task: "Unit test for list operations in tests/unit/test_repository.py"

# Launch all models for User Story 1 together:
Task: "Implement add todo functionality in src/application/services.py"
Task: "Implement list all todos functionality in src/application/services.py"
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
6. Each story adds value without breaking previous stories

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