# Quickstart Guide: In-Memory Python Console Todo App

A simple, in-memory todo management CLI built for Python learners.

## Prerequisites

- **Python**: Version 3.13 or higher
- **UV**: Recommended package manager (or use pip)

## Installation

### Option 1: Using UV (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd Hackathon-II-Phase-I-Todo-Console-app

# Initialize or sync the project
uv sync
```

### Option 2: Using pip

```bash
# Clone the repository
git clone <repository-url>
cd Hackathon-II-Phase-I-Todo-Console-app

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -e .
```

## Running the Application

### Interactive Mode (Default)

Run without arguments to enter interactive mode:

```bash
python -m src.main
# or
todo
```

Interactive mode accepts commands one at a time:

```
> todo add "Learn Python"
Added todo #1

> todo list
1. [ ] Learn Python

> todo complete 1
Completed todo #1

> todo help
Available commands:
  add <text>     - Add a new todo
  list           - List all todos
  complete <id>  - Mark todo as complete
  update <id> <text> - Update todo text
  delete <id>    - Delete a todo
  help           - Show this help
  quit           - Exit the application
```

### Single Command Mode

Pass arguments directly for non-interactive use:

```bash
python -m src.main add "Learn Python"
python -m src.main list
python -m src.main complete 1
python -m src.main delete 1
```

### Help

```bash
python -m src.main --help
```

## Usage Examples

### Adding Todos

```bash
$ todo add "Learn Python basics"
Added todo #1

$ todo add "Build a todo app"
Added todo #2

$ todo add "Write tests"
Added todo #3
```

### Viewing Todos

```bash
$ todo list

My Todo List
============

1. [ ] Learn Python basics        (created: 2026-01-04 10:30)
2. [ ] Build a todo app           (created: 2026-01-04 10:31)
3. [ ] Write tests                (created: 2026-01-04 10:32)

Total: 3 todos (0 completed, 3 pending)
```

### Marking as Complete

```bash
$ todo complete 1
Completed todo #1

$ todo list

My Todo List
============

1. [X] Learn Python basics        (created: 2026-01-04 10:30)
2. [ ] Build a todo app           (created: 2026-01-04 10:31)
3. [ ] Write tests                (created: 2026-01-04 10:32)

Total: 3 todos (1 completed, 2 pending)
```

### Updating Todos

```bash
$ todo update 2 "Build a CLI todo app"
Updated todo #2
```

### Deleting Todos

```bash
$ todo delete 3
Deleted todo #3
```

## Project Structure

```
todo-cli/
├── src/
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── parser.py      # Command-line argument parsing
│   │   └── formatter.py   # Output formatting
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── models.py      # TodoItem dataclass
│   │   └── repository.py  # In-memory storage
│   ├── application/
│   │   ├── __init__.py
│   │   └── services.py    # Business logic
│   └── main.py            # Entry point
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_models.py
│   │   ├── test_repository.py
│   │   └── test_services.py
│   └── integration/
│       └── test_cli.py
├── pyproject.toml
└── README.md
```

## Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/unit/test_models.py
```

## Development

### Adding a New Command

1. Add the command handler in `src/application/services.py`
2. Add argument parsing in `src/cli/parser.py`
3. Add output formatting in `src/cli/formatter.py` (if needed)
4. Add tests in `tests/`
5. Update this quickstart and help text

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all function signatures
- Write docstrings for public functions
- Run linting: `ruff check src/`

## Troubleshooting

### "python: command not found"

Make sure Python 3.13+ is installed and in your PATH:
```bash
python --version  # Should show 3.13.x
```

### "ModuleNotFoundError"

Ensure dependencies are installed:
```bash
uv sync  # or pip install -e .
```

### Commands not working

Verify you're running from the project root directory.

## Next Steps

This Phase I application is the foundation for future enhancements:

- **Phase II**: Add web API with FastAPI
- **Phase III**: Add AI-powered chatbot
- **Phase IV**: Deploy to Kubernetes
- **Phase V**: Cloud-native architecture

The clean layered architecture (CLI → Application → Domain) makes it easy to extend.
