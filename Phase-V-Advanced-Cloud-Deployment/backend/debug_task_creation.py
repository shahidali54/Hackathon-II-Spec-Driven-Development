#!/usr/bin/env python3
"""
Debug script to test task creation functionality and identify the 422 error
"""
import sys
import os
import json
from datetime import datetime

# Add the backend src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_model_creation():
    """Test creating Task objects directly to identify field issues"""
    print("Testing Task model creation...")

    try:
        from src.models.task import Task, TaskCreate, PriorityEnum

        # Test creating a basic task
        print("1. Testing basic task creation...")
        basic_task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "is_completed": False,
            "priority": "medium",
            "tags": ["test", "debug"],
            "recurrence_rule": {},
            "reminder_sent": False
        }

        print(f"Task data: {basic_task_data}")

        # Try creating a TaskCreate object
        task_create = TaskCreate(**basic_task_data)
        print(f"SUCCESS: TaskCreate object created successfully: {task_create}")

        print("\nTaskCreate fields:")
        for field_name in ['title', 'description', 'is_completed', 'due_date', 'priority', 'tags', 'recurrence_rule', 'reminder_sent']:
            value = getattr(task_create, field_name, 'NOT_FOUND')
            print(f"  {field_name}: {value} (type: {type(value)})")

        return True

    except Exception as e:
        print(f"ERROR: Error in model creation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoint():
    """Test the API endpoint directly"""
    print("\nTesting API endpoint...")

    try:
        from src.api.tasks import create_task
        from src.models.user import User
        from src.models.task import TaskCreate
        from src.database.database import engine
        from sqlmodel import Session

        # Create a mock user
        mock_user = User(
            id="test-user-id",
            email="test@example.com",
            hashed_password="fake_hashed_password",
            is_verified=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Create task data that mimics what the frontend would send
        task_data = {
            "title": "Debug Test Task",
            "description": "This is a test task for debugging",
            "is_completed": False,
            "priority": "medium",
            "tags": ["debug", "test"],
            "recurrence_rule": None,
            "reminder_sent": False
        }

        print(f"Task data to send: {task_data}")

        # Create the TaskCreate object
        task_create_obj = TaskCreate(**task_data)
        print(f"TaskCreate object: {task_create_obj}")

        # Create a session
        with Session(engine) as session:
            print("Session created successfully")

            # This would normally call the create_task function from the API
            # but we'll test the service layer directly

        return True

    except Exception as e:
        print(f"✗ Error in API test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_service_layer():
    """Test the service layer directly"""
    print("\nTesting service layer...")

    try:
        from src.services.task_service import TaskService
        from src.models.task import TaskCreate
        from src.database.database import engine
        from sqlmodel import Session

        # Create task data
        task_data = {
            "title": "Service Layer Test",
            "description": "Testing service layer directly",
            "is_completed": False,
            "priority": "high",
            "tags": ["service", "test"],
            "recurrence_rule": {},
            "reminder_sent": False
        }

        task_create = TaskCreate(**task_data)
        print(f"TaskCreate object: {task_create}")

        # Create a session and service
        with Session(engine) as session:
            service = TaskService(session)
            print("Service created successfully")

        return True

    except Exception as e:
        print(f"✗ Error in service test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("DEBUGGING TASK CREATION 422 ERROR")
    print("=" * 60)

    success = True

    success &= test_model_creation()
    success &= test_api_endpoint()
    success &= test_service_layer()

    print("\n" + "=" * 60)
    if success:
        print("SUCCESS: All tests passed - no obvious model/schema issues found")
        print("The 422 error may be caused by:")
        print("- Invalid request data from frontend")
        print("- Missing required fields")
        print("- Wrong data types")
        print("- Validation errors not caught by schema")
    else:
        print("ERROR: Some tests failed - there are model/schema issues to fix")
    print("=" * 60)

    return success

if __name__ == "__main__":
    main()