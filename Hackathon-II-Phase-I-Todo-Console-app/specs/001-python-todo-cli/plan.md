# Implementation Plan: In-Memory Python Console Todo App

**Branch**: `001-python-todo-cli` | **Date**: 2026-01-04 | **Spec**: [link](spec.md)
**Input**: Feature specification from `/specs/001-python-todo-cli/spec.md`

## Summary

A simple, in-memory Python console application for todo management. Users can add, view, update, delete, and mark todos as complete through a clean CLI interface. The application uses a layered architecture (CLI, Application, Domain) and stores all data in memory without persistence. Built for Python learners as a foundational project that can evolve into more complex phases.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (standard library only)
**Storage**: In-memory Python list/dict (no persistence)
**Testing**: pytest (unit tests for models and services)
**Target Platform**: Cross-platform (Windows, macOS, Linux) via Python standard library
**Project Type**: Single project (console application)
**Performance Goals**: Command execution under 1 second, minimal memory footprint (<50MB)
**Constraints**: Console-only, in-memory, no external services, no AI features
**Scale/Scope**: Single user, single session, unlimited todos per session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Compliance | Notes |
|-----------|------------|-------|
| I. Spec-Driven Development | ✅ PASS | Feature spec exists with clear requirements |
| II. Incremental Evolution | ✅ PASS | Phase I focused on core CLI, sets foundation for future phases |
| III. Simplicity First | ✅ PASS | Standard library only, no premature complexity |
| IV. Clear Separation of Concerns | ✅ PASS | Three-layer architecture (CLI, Application, Domain) |
| V. Deterministic Behavior | ✅ PASS | No AI, predictable command outputs |
| VI. Code Quality Standards | ✅ PASS | Modular structure enables testability |

**Result**: All gates pass. No violations requiring justification.

## Project Structure

### Documentation (this feature)

```text
specs/001-python-todo-cli/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (N/A - no clarifications needed)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (N/A - no external API)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code

```text
src/
├── cli/
│   ├── __init__.py
│   ├── parser.py        # Command-line argument parsing
│   └── formatter.py     # Output formatting and display
├── domain/
│   ├── __init__.py
│   ├── models.py        # TodoItem dataclass/model
│   └── repository.py    # In-memory todo storage
├── application/
│   ├── __init__.py
│   └── services.py      # Business logic for CRUD operations
└── main.py              # Entry point, CLI loop

tests/
├── __init__.py
├── unit/
│   ├── test_models.py   # TodoItem model tests
│   ├── test_repository.py
│   └── test_services.py
└── integration/
    └── test_cli.py      # End-to-end CLI tests

pyproject.toml           # UV package configuration
README.md                # User-facing documentation
```

**Structure Decision**: Single project with 3-layer architecture at `src/` root. This structure supports future evolution (e.g., adding an API layer for Phase II) without restructuring. The separation between CLI, Application, and Domain layers enables independent testing and future extensibility.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. The architecture follows all constitution principles with no deviations requiring justification.

---

## Phase 0: Research

No research needed. The feature specification and user-provided architecture are complete with no `[NEEDS CLARIFICATION]` markers. The requirements are straightforward CLI operations using standard Python patterns.

---

## Phase 1: Design & Contracts

### Data Model

The `data-model.md` file documents the TodoItem entity with its fields, validation rules, and relationships.

### Quickstart Guide

The `quickstart.md` file provides setup and run instructions for new developers.

### Contracts

Not applicable for this phase. There is no external API - the CLI is the interface.

---

## Data Model

### Entity: TodoItem

Represents a single task in the todo list.

**Fields**:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | int | auto-increment, unique | Sequential identifier for command references |
| `title` | str | 1-200 characters, non-empty | The task description |
| `completed` | bool | default False | Whether the task is done |
| `created_at` | datetime | auto-set on creation | Timestamp for ordering |

**Validation Rules**:
- Title MUST be non-empty after stripping whitespace
- Title MUST NOT exceed 200 characters
- ID MUST be unique within the session
- New items are assigned the next available ID (highest + 1)

**State Transitions**:

```
PENDING → COMPLETE (mark complete)
COMPLETE → PENDING (unmark, if supported in future)
DELETE (removes from collection)
```

### Repository: InMemoryTodoStore

Manages todo item storage and retrieval.

**Operations**:

| Operation | Parameters | Returns | Description |
|-----------|------------|---------|-------------|
| `add(item)` | TodoItem | int (new id) | Stores item, returns assigned ID |
| `get(id)` | int | TodoItem or None | Retrieves item by ID |
| `list_all()` | None | List[TodoItem] | Returns all items in creation order |
| `update(id, title)` | int, str | bool (success) | Updates item title |
| `mark_complete(id)` | int | bool (success) | Sets completed=True |
| `delete(id)` | int | bool (success) | Removes item from store |

**Design Decision**: Using a Python list for storage maintains insertion order and provides O(n) lookup by ID. For a CLI app with typical usage (<100 todos), this is simpler and more Pythonic than a dict-based approach.

### CLI Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `add <text>` | todo text | Create a new todo |
| `list` | none | Show all todos |
| `complete <id>` | todo ID | Mark todo as complete |
| `update <id> <text>` | ID and new text | Update todo text |
| `delete <id>` | todo ID | Remove todo |
| `help` | none | Show available commands |

---

## Quickstart Guide

### Prerequisites

- Python 3.13 or higher
- UV package manager (recommended) or pip

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Hackathon-II-Phase-I-Todo-Console-app

# Initialize UV project (if pyproject.toml doesn't exist)
uv init --python 3.13

# Install dependencies (currently none beyond standard library)
uv sync
```

### Running the Application

```bash
# Run in interactive mode
python -m src.main

# Or add to PATH and run directly
todo --help
```

### Usage Examples

```bash
# Add a todo
$ todo add "Learn Python"

# List all todos
$ todo list
1. [ ] Learn Python

# Mark as complete
$ todo complete 1

# Update a todo
$ todo update 1 "Learn Python basics"

# Delete a todo
$ todo delete 1

# Get help
$ todo help
```

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

---

## Next Steps

Run `/sp.tasks` to generate the implementation task list based on this plan.
