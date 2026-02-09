from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, status
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..models.user import User
import logging

# Try to import KafkaProducerService and ReminderService, but handle the case where they're not available
try:
    from .kafka_producer import KafkaProducerService
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

try:
    from .reminder_service import ReminderService
except ImportError:
    # Define a mock ReminderService for when it's not available
    class ReminderService:
        def __init__(self, db_session, kafka_producer=None):
            pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskService:
    def __init__(self, db_session: Session, kafka_producer: KafkaProducerService = None):
        self.db_session = db_session
        self.kafka_producer = kafka_producer

    def create_task(self, task_create: TaskCreate, user_id: str) -> Task:
        # Add detailed logging to identify which field causes the error
        try:
            logger.info(f"Creating task with data: {task_create.dict() if hasattr(task_create, 'dict') else task_create}")

            # Prepare the data for validation
            title = getattr(task_create, 'title', None)
            description = getattr(task_create, 'description', None)
            is_completed = getattr(task_create, 'is_completed', False)
            due_date = getattr(task_create, 'due_date', None)
            priority = getattr(task_create, 'priority', "medium")
            tags = getattr(task_create, 'tags', [])
            recurrence_rule = getattr(task_create, 'recurrence_rule', {})
            reminder_sent = getattr(task_create, 'reminder_sent', False)

            logger.info(f"Task data - title: {title}, priority: {priority}, tags: {tags}, recurrence_rule: {recurrence_rule}")

            # Create the task with the specified user_id
            db_task = Task(
                title=title,
                description=description,
                is_completed=is_completed,
                due_date=due_date,
                priority=str(priority) if priority else "medium",
                tags=tags if tags else [],
                recurrence_rule=recurrence_rule if recurrence_rule else {},
                reminder_sent=reminder_sent if reminder_sent else False,
                user_id=user_id
            )

            logger.info(f"Task object created successfully, about to add to session")
        except Exception as e:
            logger.error(f"Error creating task object: {str(e)}")
            logger.error(f"Task create object type: {type(task_create)}")
            logger.error(f"Task create object: {task_create}")
            raise HTTPException(status_code=422, detail=f"Invalid task data: {str(e)}")

        try:
            self.db_session.add(db_task)
            self.db_session.commit()
            self.db_session.refresh(db_task)
            logger.info(f"Task added to DB successfully with ID: {db_task.id}")
        except Exception as e:
            logger.error(f"Error saving task to database: {str(e)}")
            self.db_session.rollback()
            raise HTTPException(status_code=422, detail=f"Database error: {str(e)}")

        # Publish task created event if Kafka producer is available
        if self.kafka_producer:
            try:
                self.kafka_producer.publish_task_event(
                    task_id=str(db_task.id),
                    event_type="task_created",
                    user_id=user_id,
                    payload={
                        "title": db_task.title,
                        "due_date": db_task.due_date.isoformat() if db_task.due_date else None,
                        "priority": db_task.priority,
                        "has_recurrence": bool(db_task.recurrence_rule)
                    }
                )
            except Exception as e:
                logger.error(f"Failed to publish task created event: {str(e)}")

        return db_task

    def get_tasks_by_user(self, user_id: str, completed: Optional[bool] = None,
                         priority: Optional[str] = None, tags: Optional[List[str]] = None,
                         due_date_from: Optional[datetime] = None, due_date_to: Optional[datetime] = None,
                         search_term: Optional[str] = None, sort_field: Optional[str] = None,
                         sort_order: Optional[str] = "asc") -> List[Task]:
        # Build query with user_id filter
        query = select(Task).where(Task.user_id == user_id)

        # Add completed filter if specified
        if completed is not None:
            query = query.where(Task.is_completed == completed)

        # Add priority filter if specified
        if priority is not None:
            query = query.where(Task.priority == priority)

        # Add tag filter if specified
        if tags:
            for tag in tags:
                # For PostgreSQL arrays, we need to use the correct operator
                query = query.where(Task.tags.op('&&')([tag]))  # && operator checks for overlap

        # Add due date range filter if specified
        if due_date_from:
            query = query.where(Task.due_date >= due_date_from)
        if due_date_to:
            query = query.where(Task.due_date <= due_date_to)

        # Add search filter if specified
        if search_term:
            search_pattern = f"%{search_term}%"
            query = query.where(Task.title.ilike(search_pattern) |
                               Task.description.ilike(search_pattern))

        # Add sorting
        if sort_field:
            if sort_order.lower() == "desc":
                query = query.order_by(getattr(Task, sort_field).desc())
            else:
                query = query.order_by(getattr(Task, sort_field).asc())
        else:
            # Default sorting by creation date, newest first
            query = query.order_by(Task.created_at.desc())

        # Execute query
        tasks = self.db_session.exec(query).all()
        return tasks

    def get_task_by_id_and_user(self, task_id: str, user_id: str) -> Optional[Task]:
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = self.db_session.exec(statement).first()
        return task

    def update_task(self, task_id: str, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
        # Get the existing task for this user
        db_task = self.get_task_by_id_and_user(task_id, user_id)

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Update only the fields that are provided in task_update
        try:
            # Get the fields that were actually set (not just default values)
            if hasattr(task_update, '__fields_set__'):
                updated_fields = task_update.__fields_set__
            else:
                # Fallback: check each field individually
                updated_fields = set()
                for field_name in ['title', 'description', 'is_completed', 'due_date', 'priority', 'tags', 'recurrence_rule', 'reminder_sent']:
                    if hasattr(task_update, field_name):
                        value = getattr(task_update, field_name)
                        if value is not None:
                            updated_fields.add(field_name)

            for field in updated_fields:
                if hasattr(task_update, field):
                    value = getattr(task_update, field)
                    if hasattr(db_task, field):
                        try:
                            setattr(db_task, field, value)
                        except Exception as e:
                            logger.error(f"Error setting field '{field}' with value '{value}': {str(e)}")
                            raise HTTPException(status_code=422, detail=f"Invalid value for field '{field}': {str(e)}")
                    else:
                        logger.warning(f"Field '{field}' not found in Task model, skipping...")
        except Exception as e:
            logger.error(f"Error updating task: {str(e)}")
            raise HTTPException(status_code=422, detail=f"Invalid update data: {str(e)}")

        # Update the updated_at timestamp
        db_task.updated_at = datetime.utcnow()

        self.db_session.add(db_task)
        self.db_session.commit()
        self.db_session.refresh(db_task)

        # Publish task updated event if Kafka producer is available
        if self.kafka_producer:
            try:
                self.kafka_producer.publish_task_event(
                    task_id=str(db_task.id),
                    event_type="task_updated",
                    user_id=user_id,
                    payload={
                        "title": db_task.title,
                        "due_date": db_task.due_date.isoformat() if db_task.due_date else None,
                        "priority": db_task.priority,
                        "is_completed": db_task.is_completed
                    }
                )
            except Exception as e:
                logger.error(f"Failed to publish task updated event: {str(e)}")

        return db_task

    def delete_task(self, task_id: str, user_id: str) -> bool:
        # Get the existing task for this user
        db_task = self.get_task_by_id_and_user(task_id, user_id)

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        self.db_session.delete(db_task)
        self.db_session.commit()

        # Publish task deleted event if Kafka producer is available
        if self.kafka_producer:
            try:
                self.kafka_producer.publish_task_event(
                    task_id=task_id,
                    event_type="task_deleted",
                    user_id=user_id,
                    payload={}
                )
            except Exception as e:
                logger.error(f"Failed to publish task deleted event: {str(e)}")

        return True

    def toggle_task_completion(self, task_id: str, completed: bool, user_id: str) -> Optional[Task]:
        # Get the existing task for this user
        db_task = self.get_task_by_id_and_user(task_id, user_id)

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Update the completion status
        db_task.is_completed = completed
        db_task.updated_at = datetime.utcnow()

        # If task has a recurrence rule and is being marked as completed,
        # schedule creation of the next occurrence
        if db_task.recurrence_rule and completed:
            self.handle_recurring_task_completion(db_task)

        self.db_session.add(db_task)
        self.db_session.commit()
        self.db_session.refresh(db_task)

        # Publish task completion event if Kafka producer is available
        if self.kafka_producer:
            try:
                self.kafka_producer.publish_task_event(
                    task_id=task_id,
                    event_type="task_completion_toggled",
                    user_id=user_id,
                    payload={
                        "is_completed": completed,
                        "title": db_task.title,
                        "has_recurrence": bool(db_task.recurrence_rule)
                    }
                )
            except Exception as e:
                logger.error(f"Failed to publish task completion event: {str(e)}")

        return db_task

    def handle_recurring_task_completion(self, completed_task: Task):
        """Handle the completion of a recurring task by creating the next occurrence"""
        if not completed_task.recurrence_rule or not completed_task.recurrence_rule.get('enabled', False):
            return

        # For now, just publish an event that the recurring task was completed
        # The actual recurring task service will handle creating the next occurrence
        if self.kafka_producer:
            try:
                self.kafka_producer.publish_recurring_task_event(
                    task_id=str(completed_task.id),
                    next_occurrence="",  # Will be calculated by the recurring task service
                    user_id=str(completed_task.user_id)
                )
            except Exception as e:
                logger.error(f"Failed to publish recurring task completion event: {str(e)}")

    def schedule_next_recurring_task(self, task: Task):
        """Schedule the next occurrence of a recurring task"""
        # This would typically involve creating an event that triggers the recurring task service
        # For now, this is a placeholder that would connect to the Kafka producer
        if self.kafka_producer:
            try:
                self.kafka_producer.publish_recurring_task_event(
                    task_id=str(task.id),
                    next_occurrence=task.due_date.isoformat() if task.due_date else "",
                    user_id=str(task.user_id)
                )
            except Exception as e:
                logger.error(f"Failed to publish recurring task event: {str(e)}")

    def search_tasks(self, user_id: str, search_term: str, limit: int = 50) -> List[Task]:
        """Search tasks by title or description for the specified user"""
        search_pattern = f"%{search_term}%"
        query = select(Task).where(
            Task.user_id == user_id
        ).where(
            Task.title.ilike(search_pattern) | Task.description.ilike(search_pattern)
        ).limit(limit)

        tasks = self.db_session.exec(query).all()

        # Publish search event if Kafka producer is available
        if self.kafka_producer:
            try:
                self.kafka_producer.publish_task_event(
                    task_id="search_operation",
                    event_type="task_search_performed",
                    user_id=user_id,
                    payload={
                        "search_term": search_term,
                        "result_count": len(tasks)
                    }
                )
            except Exception as e:
                logger.error(f"Failed to publish search event: {str(e)}")

        return tasks

    def schedule_task_reminder(self, task_id: str, reminder_time: datetime, user_id: str):
        """Schedule a reminder for a task"""
        if self.kafka_producer:
            try:
                self.kafka_producer.publish_reminder_event(
                    task_id=task_id,
                    reminder_time=reminder_time.isoformat(),
                    user_id=user_id
                )
            except Exception as e:
                logger.error(f"Failed to publish reminder event: {str(e)}")

        # In a real implementation, we would also store the reminder in the database
        # and potentially schedule it in a scheduler service

    def handle_recurring_task_completion(self, completed_task: Task):
        """Handle the completion of a recurring task by creating the next occurrence"""
        if not completed_task.recurrence_rule or not completed_task.recurrence_rule.get('enabled', False):
            return

        # For now, just publish an event that the recurring task was completed
        # The actual recurring task service will handle creating the next occurrence
        if self.kafka_producer:
            try:
                self.kafka_producer.publish_recurring_task_event(
                    task_id=str(completed_task.id),
                    next_occurrence="",  # Will be calculated by the recurring task service
                    user_id=str(completed_task.user_id)
                )
            except Exception as e:
                logger.error(f"Failed to publish recurring task completion event: {str(e)}")