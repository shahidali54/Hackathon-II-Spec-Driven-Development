from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from ..database.database import engine
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..models.reminder import Reminder
from ..models.user import User
from ..services.task_service import TaskService
from ..services.reminder_service import ReminderService
from ..services.recurring_service import RecurringTaskService
from ..api.deps import get_current_user
from datetime import datetime
import uuid

# Try to import KafkaProducerService, but handle the case where it's not available
try:
    from ..services.kafka_producer import KafkaProducerService
except ImportError:
    # Define a mock KafkaProducerService for when confluent-kafka is not available
    class KafkaProducerService:
        def __init__(self, bootstrap_servers: str = "localhost:9092"):
            pass

        def publish_task_event(self, task_id: str, event_type: str, user_id: str, payload: dict = None):
            # Mock implementation
            print(f"MOCK: Would publish task event {event_type} for task {task_id}")

        def publish_reminder_event(self, task_id: str, reminder_time: str, user_id: str):
            # Mock implementation
            print(f"MOCK: Would publish reminder event for task {task_id}")

        def publish_recurring_task_event(self, task_id: str, next_occurrence: str, user_id: str):
            # Mock implementation
            print(f"MOCK: Would publish recurring task event for task {task_id}")

        def publish_event(self, topic: str, event_data: dict):
            # Mock implementation
            print(f"MOCK: Would publish event to topic {topic}")


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


def get_kafka_producer():
    # Create and return a Kafka producer instance
    # In a real implementation, you might want to get this from a dependency injection container
    try:
        return KafkaProducerService()
    except Exception as e:
        # Log the error and return None if Kafka is not available
        print(f"Warning: Could not initialize Kafka producer: {e}")
        return None


router = APIRouter()

@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    completed: Optional[bool] = Query(None, description="Filter tasks by completion status"),
    priority: Optional[str] = Query(None, description="Filter tasks by priority level"),
    tags: Optional[str] = Query(None, description="Filter tasks by tags (comma-separated)"),
    due_date_from: Optional[datetime] = Query(None, description="Filter tasks with due date on or after this date"),
    due_date_to: Optional[datetime] = Query(None, description="Filter tasks with due date on or before this date"),
    search: Optional[str] = Query(None, description="Search term to filter tasks by title or description"),
    sort: Optional[str] = Query(None, description="Field to sort by"),
    order: Optional[str] = Query("asc", description="Sort order (asc or desc)"),
    limit: Optional[int] = Query(50, ge=1, le=100, description="Maximum number of tasks to return"),
    offset: Optional[int] = Query(0, ge=0, description="Number of tasks to skip"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.
    The user is identified from the JWT token.
    """

    # Parse tags from comma-separated string if provided
    parsed_tags = None
    if tags:
        parsed_tags = [tag.strip() for tag in tags.split(",")]

    kafka_producer = get_kafka_producer()
    task_service = TaskService(session, kafka_producer=kafka_producer)

    tasks = task_service.get_tasks_by_user(
        user_id=str(current_user.id),
        completed=completed,
        priority=priority,
        tags=parsed_tags,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        search_term=search,
        sort_field=sort,
        sort_order=order
    )

    # Apply pagination (limit and offset)
    paginated_tasks = tasks[offset:offset+limit]

    return paginated_tasks

@router.post("/tasks", response_model=TaskRead)
def create_task(
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    The user is identified from the JWT token.
    """

    kafka_producer = get_kafka_producer()
    task_service = TaskService(session, kafka_producer=kafka_producer)
    db_task = task_service.create_task(task_create, str(current_user.id))

    return db_task

@router.get("/tasks/{id}", response_model=TaskRead)
def get_task(
    id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the authenticated user.
    The user is identified from the JWT token.
    """

    task_service = TaskService(session)
    db_task = task_service.get_task_by_id_and_user(id, str(current_user.id))

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return db_task

@router.put("/tasks/{id}", response_model=TaskRead)
def update_task(
    id: str,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update all details of a specific task for the authenticated user.
    The user is identified from the JWT token.
    """

    kafka_producer = get_kafka_producer()
    task_service = TaskService(session, kafka_producer=kafka_producer)
    updated_task = task_service.update_task(id, task_update, str(current_user.id))

    return updated_task

@router.delete("/tasks/{id}")
def delete_task(
    id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the authenticated user.
    The user is identified from the JWT token.
    """

    kafka_producer = get_kafka_producer()
    task_service = TaskService(session, kafka_producer=kafka_producer)
    success = task_service.delete_task(id, str(current_user.id))

    if success:
        return {"message": "Task deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

@router.patch("/tasks/{id}/complete", response_model=TaskRead)
def toggle_task_completion(
    id: str,
    completed: bool,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific task for the authenticated user.
    The user is identified from the JWT token.
    """

    kafka_producer = get_kafka_producer()
    task_service = TaskService(session, kafka_producer=kafka_producer)
    updated_task = task_service.toggle_task_completion(id, completed, str(current_user.id))

    return updated_task

# Additional endpoints for advanced features

@router.get("/tasks/search", response_model=List[TaskRead])
def search_tasks(
    q: str = Query(..., description="Search query"),
    limit: Optional[int] = Query(50, ge=1, le=100, description="Maximum number of tasks to return"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Search tasks by title or description for the authenticated user.
    """

    kafka_producer = get_kafka_producer()
    task_service = TaskService(session, kafka_producer=kafka_producer)
    tasks = task_service.search_tasks(str(current_user.id), q, limit)

    return tasks

@router.get("/tasks/filter", response_model=List[TaskRead])
def filter_tasks(
    priority: Optional[str] = Query(None, description="Filter by priority level"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated)"),
    due_date_from: Optional[datetime] = Query(None, description="Filter by due date from"),
    due_date_to: Optional[datetime] = Query(None, description="Filter by due date to"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    sort: Optional[str] = Query(None, description="Sort by field"),
    order: Optional[str] = Query("asc", description="Sort order (asc or desc)"),
    limit: Optional[int] = Query(50, ge=1, le=100, description="Maximum number of tasks to return"),
    offset: Optional[int] = Query(0, ge=0, description="Number of tasks to skip"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Filter tasks by multiple criteria for the authenticated user.
    """

    # Parse tags from comma-separated string if provided
    parsed_tags = None
    if tags:
        parsed_tags = [tag.strip() for tag in tags.split(",")]

    kafka_producer = get_kafka_producer()
    task_service = TaskService(session, kafka_producer=kafka_producer)
    tasks = task_service.get_tasks_by_user(
        user_id=str(current_user.id),
        completed=completed,
        priority=priority,
        tags=parsed_tags,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        search_term=None,  # No search term for filter endpoint
        sort_field=sort,
        sort_order=order
    )

    # Apply pagination
    paginated_tasks = tasks[offset:offset+limit]

    return paginated_tasks


# Reminder Management Endpoints

@router.post("/tasks/{task_id}/reminders")
def create_reminder(
    task_id: str,
    remind_at: datetime = Query(..., description="Time to send the reminder"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a reminder for a specific task.
    """
    # Verify the task belongs to the current user
    task_service = TaskService(session)
    db_task = task_service.get_task_by_id_and_user(task_id, str(current_user.id))
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    kafka_producer = get_kafka_producer()
    reminder_service = ReminderService(session, kafka_producer=kafka_producer)
    
    try:
        from ..schemas.reminder import ReminderCreate as ReminderCreateSchema
        reminder_data = ReminderCreateSchema(
            task_id=uuid.UUID(task_id),
            remind_at=remind_at,
            sent=False
        )
        reminder = reminder_service.create_reminder(reminder_data)
        return {"id": str(reminder.id), "task_id": str(reminder.task_id), "remind_at": reminder.remind_at}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/tasks/{task_id}/reminders")
def get_task_reminders(
    task_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all reminders for a specific task.
    """
    # Verify the task belongs to the current user
    task_service = TaskService(session)
    db_task = task_service.get_task_by_id_and_user(task_id, str(current_user.id))
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    reminder_service = ReminderService(session)
    reminders = reminder_service.get_reminders_for_task(uuid.UUID(task_id))
    
    return [{"id": str(r.id), "task_id": str(r.task_id), "remind_at": r.remind_at, "sent": r.sent} for r in reminders]

@router.delete("/reminders/{reminder_id}")
def delete_reminder(
    reminder_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific reminder.
    """
    reminder_service = ReminderService(session)
    
    try:
        reminder_id_uuid = uuid.UUID(reminder_id)
        success = reminder_service.delete_reminder(reminder_id_uuid)
        if success:
            return {"message": "Reminder deleted successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid reminder ID")

@router.get("/reminders/upcoming")
def get_upcoming_reminders(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all upcoming reminders for the current user that haven't been sent.
    """
    reminder_service = ReminderService(session)
    reminders = reminder_service.get_reminders_by_user(str(current_user.id))
    upcoming = [r for r in reminders if not r.sent and r.remind_at > datetime.utcnow()]
    
    return [{"id": str(r.id), "task_id": str(r.task_id), "remind_at": r.remind_at} for r in upcoming]
