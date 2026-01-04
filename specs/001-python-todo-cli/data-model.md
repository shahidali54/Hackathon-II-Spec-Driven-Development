# Data Model: In-Memory Python Console Todo App

## Entity: TodoItem

Represents a single task in the todo list.

### Fields

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `id` | int | auto-increment, unique | auto-generated | Sequential identifier for command references |
| `title` | str | 1-200 chars, non-empty | N/A | The task description |
| `completed` | bool | N/A | False | Whether the task is done |
| `created_at` | datetime | auto-set on creation | auto-generated | Timestamp for ordering |

### Validation Rules

- Title MUST be non-empty after stripping whitespace
- Title MUST NOT exceed 200 characters
- ID MUST be unique within the session
- New items are assigned the next available ID (highest existing + 1)

### State Transitions

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   PENDING ──────────► COMPLETE                              │
│      ▲               (mark_complete)                        │
│      │                                                       │
│      │                                                       │
│      │                                                       │
│      └─────────── DELETE                                    │
│                    (removes from collection)                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Python Implementation (dataclass)

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class TodoItem:
    """Represents a single todo item."""
    title: str
    id: int = 0
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        """Validate after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        if len(self.title) > 200:
            raise ValueError("Title cannot exceed 200 characters")
```

## Repository: InMemoryTodoStore

Manages todo item storage and retrieval.

### Design Decision

Using a Python list for storage maintains insertion order and provides O(n) lookup by ID. For a CLI app with typical usage (<100 todos), this is simpler and more Pythonic than a dict-based approach.

### Operations

| Operation | Parameters | Returns | Description |
|-----------|------------|---------|-------------|
| `add(item)` | TodoItem | int (new id) | Stores item, returns assigned ID |
| `get(id)` | int | TodoItem or None | Retrieves item by ID |
| `list_all()` | None | List[TodoItem] | Returns all items in creation order |
| `list_pending()` | None | List[TodoItem] | Returns only incomplete items |
| `list_completed()` | None | List[TodoItem] | Returns only complete items |
| `update(id, title)` | int, str | bool (success) | Updates item title |
| `mark_complete(id)` | int | bool (success) | Sets completed=True |
| `mark_incomplete(id)` | int | bool (success) | Sets completed=False |
| `delete(id)` | int | bool (success) | Removes item from store |
| `count()` | None | int | Returns total item count |
| `clear()` | None | None | Removes all items |

### Python Implementation

```python
from typing import List, Optional

class InMemoryTodoStore:
    """In-memory storage for todo items."""

    def __init__(self):
        self._items: List[TodoItem] = []
        self._next_id: int = 1

    def add(self, item: TodoItem) -> int:
        """Add a new todo item."""
        item.id = self._next_id
        self._next_id += 1
        self._items.append(item)
        return item.id

    def get(self, todo_id: int) -> Optional[TodoItem]:
        """Retrieve a todo by ID."""
        for item in self._items:
            if item.id == todo_id:
                return item
        return None

    def list_all(self) -> List[TodoItem]:
        """Return all todos in creation order."""
        return self._items.copy()

    def list_pending(self) -> List[TodoItem]:
        """Return only incomplete todos."""
        return [item for item in self._items if not item.completed]

    def list_completed(self) -> List[TodoItem]:
        """Return only completed todos."""
        return [item for item in self._items if item.completed]

    def update(self, todo_id: int, title: str) -> bool:
        """Update a todo's title."""
        item = self.get(todo_id)
        if item:
            item.title = title
            return True
        return False

    def mark_complete(self, todo_id: int) -> bool:
        """Mark a todo as complete."""
        item = self.get(todo_id)
        if item:
            item.completed = True
            return True
        return False

    def mark_incomplete(self, todo_id: int) -> bool:
        """Mark a todo as incomplete."""
        item = self.get(todo_id)
        if item:
            item.completed = False
            return True
        return False

    def delete(self, todo_id: int) -> bool:
        """Delete a todo by ID."""
        item = self.get(todo_id)
        if item:
            self._items.remove(item)
            return True
        return False

    def count(self) -> int:
        """Return total number of todos."""
        return len(self._items)

    def clear(self) -> None:
        """Remove all todos."""
        self._items.clear()
        self._next_id = 1
```

## Output Format

### List Command Output

```
$ todo list

My Todo List
============

1. [ ] Learn Python                     (created: 2026-01-04 10:30)
2. [X] Set up project structure         (created: 2026-01-04 10:25)
3. [ ] Write unit tests                 (created: 2026-01-04 10:35)

Total: 3 todos (1 completed, 2 pending)
```

### Error Messages

| Scenario | Message |
|----------|---------|
| Todo not found | "Error: Todo with ID {id} not found" |
| Empty title | "Error: Todo title cannot be empty" |
| Title too long | "Error: Todo title cannot exceed 200 characters" |
| Invalid ID format | "Error: Invalid ID '{input}'. Must be a number." |
