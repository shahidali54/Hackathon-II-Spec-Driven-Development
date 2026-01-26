"""Todo Console Application - Single Interactive Program"""

from datetime import datetime
from typing import List, Optional


class TodoItem:
    """Represents a single todo item."""
    def __init__(self, title: str, todo_id: int = 0, completed: bool = False):
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        if len(title) > 200:
            raise ValueError("Title cannot exceed 200 characters")

        self.id = todo_id
        self.title = title.strip()
        self.completed = completed
        self.created_at = datetime.now()


class TodoStore:
    """In-memory storage for todo items."""
    def __init__(self):
        self._items: List[TodoItem] = []
        self._next_id = 1

    def add(self, title: str) -> int:
        """Add a new todo item."""
        item = TodoItem(title, self._next_id)
        self._items.append(item)
        todo_id = self._next_id
        self._next_id += 1
        return todo_id

    def get_all(self) -> List[TodoItem]:
        """Get all todos."""
        return self._items.copy()

    def get_by_id(self, todo_id: int) -> Optional[TodoItem]:
        """Get a todo by ID."""
        for item in self._items:
            if item.id == todo_id:
                return item
        return None

    def update(self, todo_id: int, title: str) -> bool:
        """Update a todo's title."""
        item = self.get_by_id(todo_id)
        if item:
            if not title or not title.strip():
                raise ValueError("Title cannot be empty")
            if len(title) > 200:
                raise ValueError("Title cannot exceed 200 characters")

            item.title = title.strip()
            return True
        return False

    def mark_complete(self, todo_id: int) -> bool:
        """Mark a todo as complete."""
        item = self.get_by_id(todo_id)
        if item:
            item.completed = True
            return True
        return False

    def delete(self, todo_id: int) -> bool:
        """Delete a todo by ID."""
        item = self.get_by_id(todo_id)
        if item:
            self._items.remove(item)
            return True
        return False

    def get_pending(self) -> List[TodoItem]:
        """Get pending todos."""
        return [item for item in self._items if not item.completed]

    def get_completed(self) -> List[TodoItem]:
        """Get completed todos."""
        return [item for item in self._items if item.completed]


class TodoApp:
    """Main todo application."""
    def __init__(self):
        self.store = TodoStore()

    def display_menu(self):
        """Display the main menu."""
        print("\n==== TODO APP ====")
        print("1. Add Todo")
        print("2. List Todos")
        print("3. Update Todo")
        print("4. Delete Todo")
        print("5. Mark Complete")
        print("6. Exit")
        print()

    def add_todo(self):
        """Add a new todo."""
        try:
            title = input("Enter todo title: ").strip()
            if not title:
                print("Error: Title cannot be empty")
                return

            todo_id = self.store.add(title)
            print(f"Added todo #{todo_id}: {title}")
        except ValueError as e:
            print(f"Error: {e}")

    def list_todos(self):
        """List all todos."""
        todos = self.store.get_all()
        if not todos:
            print("\nNo todos found.")
            return

        print("\nYour Todos:")
        print("-" * 60)
        for todo in todos:
            status = "X" if todo.completed else "O"
            created_str = todo.created_at.strftime("%Y-%m-%d %H:%M")
            print(f"{todo.id}. [{status}] {todo.title} (added: {created_str})")
        print("-" * 60)
        print(f"Total: {len(todos)} todos")

    def update_todo(self):
        """Update a todo."""
        try:
            if not self.store.get_all():
                print("No todos to update.")
                return

            self.list_todos()
            todo_id = int(input("Enter todo ID to update: "))

            todo = self.store.get_by_id(todo_id)
            if not todo:
                print(f"Error: Todo with ID {todo_id} not found")
                return

            new_title = input(f"Enter new title for todo #{todo_id}: ").strip()
            if not new_title:
                print("Error: Title cannot be empty")
                return

            self.store.update(todo_id, new_title)
            print(f"Updated todo #{todo_id} to: {new_title}")
        except ValueError:
            print("Error: Please enter a valid todo ID (number)")

    def delete_todo(self):
        """Delete a todo."""
        try:
            if not self.store.get_all():
                print("No todos to delete.")
                return

            self.list_todos()
            todo_id = int(input("Enter todo ID to delete: "))

            if self.store.delete(todo_id):
                print(f"Deleted todo #{todo_id}")
            else:
                print(f"Error: Todo with ID {todo_id} not found")
        except ValueError:
            print("Error: Please enter a valid todo ID (number)")

    def mark_complete(self):
        """Mark a todo as complete."""
        try:
            if not self.store.get_all():
                print("No todos to mark complete.")
                return

            self.list_todos()
            todo_id = int(input("Enter todo ID to mark complete: "))

            if self.store.mark_complete(todo_id):
                print(f"Marked todo #{todo_id} as complete")
            else:
                print(f"Error: Todo with ID {todo_id} not found")
        except ValueError:
            print("Error: Please enter a valid todo ID (number)")

    def run(self):
        """Run the main application loop."""
        print("Welcome to the Todo App!")
        while True:
            self.display_menu()
            try:
                choice = input("Select an option: ").strip()

                if choice == "1":
                    self.add_todo()
                elif choice == "2":
                    self.list_todos()
                elif choice == "3":
                    self.update_todo()
                elif choice == "4":
                    self.delete_todo()
                elif choice == "5":
                    self.mark_complete()
                elif choice == "6":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid option. Please select 1-6.")
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break


def main():
    """Main entry point."""
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()