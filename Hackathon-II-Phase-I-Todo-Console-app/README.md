# Todo Console Application

A simple, in-memory todo management console application built for Python learners.

## Features

- Add, list, update, complete, and delete todos
- All data stored in-memory (no persistence)
- Single interactive console program
- Clean, menu-driven interface
- Cross-platform compatibility

## Prerequisites

- Python 3.13 or higher

## Usage

Run the application:

```bash
python main.py
```

The application will start in interactive mode with a menu:

```
==== TODO APP ====
1. Add Todo
2. List Todos
3. Update Todo
4. Delete Todo
5. Mark Complete
6. Exit

Select an option:
```

## Functionality

### Adding Todos

1. Select option `1` from the menu
2. Enter the todo title when prompted
3. The todo will be added with an auto-generated ID

### Viewing Todos

1. Select option `2` from the menu
2. All todos will be displayed with their status (O = pending, X = complete)

### Marking as Complete

1. Select option `5` from the menu
2. Enter the todo ID when prompted
3. The todo will be marked as complete

### Updating Todos

1. Select option `3` from the menu
2. Enter the todo ID when prompted
3. Enter the new title when prompted

### Deleting Todos

1. Select option `4` from the menu
2. Enter the todo ID when prompted
3. The todo will be deleted

## Architecture

The application is a single interactive console program with:

- **TodoItem**: Represents a single todo item
- **TodoStore**: In-memory storage for todos
- **TodoApp**: Main application with menu loop
- **main()**: Entry point that starts the application

All data is stored in memory only and will be lost when the application exits.

## Project Structure

```
todo-console-app/
├── main.py        # Single entry point with all functionality
└── README.md
```

## Next Steps

This Phase I application is the foundation for future enhancements:

- **Phase II**: Add web API with FastAPI
- **Phase III**: Add AI-powered chatbot
- **Phase IV**: Deploy to Kubernetes
- **Phase V**: Cloud-native architecture
