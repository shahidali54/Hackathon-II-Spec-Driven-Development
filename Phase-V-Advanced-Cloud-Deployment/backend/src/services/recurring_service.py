from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import HTTPException, status
import uuid
from ..models.task import Task
from ..models.recurring_task_pattern import RecurringTaskPattern, RecurringTaskPatternCreate
from ..schemas.recurring_task_pattern import RecurringTaskPatternCreate as RecurringTaskPatternSchemaCreate
from ..schemas.task import TaskCreate as TaskSchemaCreate
import json
import logging

# Try to import KafkaProducerService, but handle the case where it's not available
try:
    from .kafka_producer import KafkaProducerService
except ImportError:
    # Define a mock KafkaProducerService for when confluent-kafka is not available
    class KafkaProducerService:
        def __init__(self, bootstrap_servers: str = "localhost:9092"):
            pass

        def publish_recurring_task_event(self, task_id: str, next_occurrence: str, user_id: str):
            # Mock implementation
            print(f"MOCK: Would publish recurring task event for task {task_id}")

        def publish_event(self, topic: str, event_data: dict):
            # Mock implementation
            print(f"MOCK: Would publish event to topic {topic}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecurringTaskService:
    def __init__(self, db_session: Session, kafka_producer: KafkaProducerService = None):
        self.db_session = db_session
        self.kafka_producer = kafka_producer

    def create_recurring_task(self, recurring_task_data: RecurringTaskPatternSchemaCreate) -> RecurringTaskPattern:
        """Create a recurring task pattern"""
        db_recurring_task = RecurringTaskPattern(
            task_id=recurring_task_data.task_id,
            rule=recurring_task_data.rule,
            next_occurrence=recurring_task_data.next_occurrence
        )

        self.db_session.add(db_recurring_task)
        self.db_session.commit()
        self.db_session.refresh(db_recurring_task)

        return db_recurring_task

    def process_completed_recurring_task(self, completed_task: Task, task_service) -> Optional[Task]:
        """Process a completed recurring task and create the next occurrence"""
        if not completed_task.recurrence_rule or not completed_task.recurrence_rule.get('enabled', False):
            return None

        # Determine when the next occurrence should be based on the recurrence rule
        next_task = self.generate_next_task_from_recurring_rule(completed_task)

        if next_task:
            # Create the new task using the task service
            new_task = task_service.create_task(next_task, str(completed_task.user_id))

            # If Kafka producer is available, publish an event
            if self.kafka_producer:
                try:
                    self.kafka_producer.publish_recurring_task_event(
                        task_id=str(new_task.id),
                        next_occurrence=new_task.due_date.isoformat() if new_task.due_date else "",
                        user_id=str(new_task.user_id)
                    )
                except Exception as e:
                    logger.error(f"Failed to publish recurring task event: {str(e)}")

            return new_task

        return None

    def generate_next_task_from_recurring_rule(self, original_task: Task) -> Optional[TaskSchemaCreate]:
        """Generate the next task based on the recurrence rule"""
        if not original_task.recurrence_rule:
            return None

        rule = original_task.recurrence_rule
        frequency = rule.get('frequency', 'daily')
        interval = rule.get('interval', 1)

        # Calculate the next occurrence date
        next_date = self.calculate_next_date(original_task.completed_at or datetime.utcnow(),
                                           frequency, interval)

        if next_date:
            # Create a new task based on the original task but with the new due date
            new_task_data = TaskSchemaCreate(
                title=original_task.title,
                description=original_task.description,
                is_completed=False,
                due_date=next_date,
                priority=original_task.priority,
                tags=original_task.tags,
                recurrence_rule=original_task.recurrence_rule,  # Carry forward the recurrence rule
                reminder_sent=False
            )

            return new_task_data

        return None

    def calculate_next_date(self, current_date: datetime, frequency: str, interval: int) -> Optional[datetime]:
        """Calculate the next occurrence date based on frequency and interval"""
        if frequency == 'daily':
            return current_date + timedelta(days=interval)
        elif frequency == 'weekly':
            return current_date + timedelta(weeks=interval)
        elif frequency == 'monthly':
            # This is a simplified version - for more complex month calculations,
            # consider using the dateutil library
            import calendar
            current_day = current_date.day
            target_month = current_date.month + interval

            # Handle year overflow
            target_year = current_date.year + (target_month - 1) // 12
            target_month = ((target_month - 1) % 12) + 1

            # Adjust for months with fewer days
            max_day = calendar.monthrange(target_year, target_month)[1]
            target_day = min(current_day, max_day)

            return current_date.replace(year=target_year, month=target_month, day=target_day)
        elif frequency == 'yearly':
            return current_date.replace(year=current_date.year + interval)
        else:
            logger.error(f"Unsupported frequency: {frequency}")
            return None

    def get_recurring_tasks_by_user(self, user_id: str) -> List[RecurringTaskPattern]:
        """Get all recurring task patterns for a specific user"""
        # Join Task and RecurringTaskPattern tables to filter by user
        statement = select(RecurringTaskPattern).join(Task).where(Task.user_id == user_id)
        recurring_tasks = self.db_session.exec(statement).all()
        return recurring_tasks