from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, status
import uuid
from ..models.reminder import Reminder, ReminderCreate
from ..models.task import Task
from ..schemas.reminder import ReminderCreate as ReminderSchemaCreate, ReminderRead
import logging

# Try to import KafkaProducerService, but handle the case where it's not available
try:
    from .kafka_producer import KafkaProducerService
except ImportError:
    # Define a mock KafkaProducerService for when confluent-kafka is not available
    class KafkaProducerService:
        def __init__(self, bootstrap_servers: str = "localhost:9092"):
            pass

        def publish_reminder_event(self, task_id: str, reminder_time: str, user_id: str):
            # Mock implementation
            print(f"MOCK: Would publish reminder event for task {task_id}")

        def publish_event(self, topic: str, event_data: dict):
            # Mock implementation
            print(f"MOCK: Would publish event to topic {topic}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReminderService:
    def __init__(self, db_session: Session, kafka_producer: KafkaProducerService = None):
        self.db_session = db_session
        self.kafka_producer = kafka_producer

    def create_reminder(self, reminder_create: ReminderSchemaCreate) -> Reminder:
        """Create a new reminder"""
        # Validate that reminder time is in the future
        if reminder_create.remind_at < datetime.utcnow():
            raise ValueError("Reminder time must be in the future")
        
        db_reminder = Reminder(
            task_id=reminder_create.task_id,
            remind_at=reminder_create.remind_at,
            sent=reminder_create.sent
        )

        self.db_session.add(db_reminder)
        self.db_session.commit()
        self.db_session.refresh(db_reminder)

        # Publish reminder created event if Kafka producer is available
        if self.kafka_producer:
            try:
                # Get the task to find user_id
                statement = select(Task).where(Task.id == reminder_create.task_id)
                task = self.db_session.exec(statement).first()
                user_id = str(task.user_id) if task else "unknown"
                
                self.kafka_producer.publish_reminder_event(
                    task_id=str(reminder_create.task_id),
                    reminder_time=reminder_create.remind_at.isoformat(),
                    user_id=user_id
                )
            except Exception as e:
                logger.error(f"Failed to publish reminder created event: {str(e)}")

        return db_reminder

    def get_reminders_for_task(self, task_id: uuid.UUID) -> List[Reminder]:
        """Get all reminders for a specific task"""
        statement = select(Reminder).where(Reminder.task_id == task_id)
        reminders = self.db_session.exec(statement).all()
        return reminders

    def get_upcoming_reminders(self, check_time: Optional[datetime] = None) -> List[Reminder]:
        """Get all upcoming reminders that haven't been sent yet"""
        if not check_time:
            check_time = datetime.utcnow()

        statement = select(Reminder).where(
            Reminder.remind_at <= check_time,
            Reminder.sent == False
        )
        reminders = self.db_session.exec(statement).all()
        return reminders

    def mark_reminder_as_sent(self, reminder_id: uuid.UUID) -> Reminder:
        """Mark a reminder as sent"""
        statement = select(Reminder).where(Reminder.id == reminder_id)
        db_reminder = self.db_session.exec(statement).first()

        if not db_reminder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reminder not found"
            )

        db_reminder.sent = True
        db_reminder.sent_at = datetime.utcnow()
        self.db_session.add(db_reminder)
        self.db_session.commit()
        self.db_session.refresh(db_reminder)

        # Publish reminder sent event if Kafka producer is available
        if self.kafka_producer:
            try:
                statement = select(Task).where(Task.id == db_reminder.task_id)
                task = self.db_session.exec(statement).first()
                user_id = str(task.user_id) if task else "unknown"
                
                self.kafka_producer.publish_reminder_event(
                    task_id=str(db_reminder.task_id),
                    reminder_time=db_reminder.remind_at.isoformat(),
                    user_id=user_id
                )
            except Exception as e:
                logger.error(f"Failed to publish reminder sent event: {str(e)}")

        return db_reminder

    def schedule_reminder(self, task_id: uuid.UUID, remind_at: datetime, user_id: str) -> Reminder:
        """Schedule a reminder for a task"""
        reminder_data = ReminderSchemaCreate(
            task_id=task_id,
            remind_at=remind_at,
            sent=False
        )

        reminder = self.create_reminder(reminder_data)

        logger.info(f"Scheduled reminder for task {task_id} at {remind_at}")

        return reminder

    def delete_reminder(self, reminder_id: uuid.UUID) -> bool:
        """Delete a reminder"""
        statement = select(Reminder).where(Reminder.id == reminder_id)
        db_reminder = self.db_session.exec(statement).first()

        if not db_reminder:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reminder not found"
            )

        self.db_session.delete(db_reminder)
        self.db_session.commit()

        logger.info(f"Deleted reminder {reminder_id}")
        return True

    def delete_all_reminders_for_task(self, task_id: uuid.UUID) -> int:
        """Delete all reminders for a specific task"""
        statement = select(Reminder).where(Reminder.task_id == task_id)
        reminders = self.db_session.exec(statement).all()

        deleted_count = 0
        for reminder in reminders:
            self.db_session.delete(reminder)
            deleted_count += 1

        self.db_session.commit()

        logger.info(f"Deleted {deleted_count} reminders for task {task_id}")
        return deleted_count

    def get_overdue_reminders(self) -> List[Reminder]:
        """Get all reminders that are overdue and not sent"""
        statement = select(Reminder).where(
            Reminder.remind_at < datetime.utcnow(),
            Reminder.sent == False
        )
        reminders = self.db_session.exec(statement).all()
        return reminders

    def get_reminders_by_user(self, user_id: str) -> List[Reminder]:
        """Get all reminders for a specific user"""
        # This would require joining with the Task table to filter by user
        # Since the Reminder model doesn't directly reference the user,
        # we'd need to join through the Task table
        from ..models.task import Task
        statement = select(Reminder).join(Task).where(Task.user_id == user_id)
        reminders = self.db_session.exec(statement).all()
        return reminders
