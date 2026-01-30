from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, status
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User

class TaskService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_task(self, task_create: TaskCreate, user_id: str) -> Task:
        # Create the task with the specified user_id
        db_task = Task(
            title=task_create.title,
            description=task_create.description,
            is_completed=task_create.is_completed,
            due_date=task_create.due_date,
            priority=task_create.priority,
            user_id=user_id
        )

        self.db_session.add(db_task)
        self.db_session.commit()
        self.db_session.refresh(db_task)

        return db_task

    def get_tasks_by_user(self, user_id: str, completed: Optional[bool] = None) -> List[Task]:
        # Build query with user_id filter
        query = select(Task).where(Task.user_id == user_id)

        # Add completed filter if specified
        if completed is not None:
            query = query.where(Task.is_completed == completed)

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
        for field, value in task_update.dict(exclude_unset=True).items():
            setattr(db_task, field, value)

        # Update the updated_at timestamp
        db_task.updated_at = datetime.utcnow()

        self.db_session.add(db_task)
        self.db_session.commit()
        self.db_session.refresh(db_task)

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

        self.db_session.add(db_task)
        self.db_session.commit()
        self.db_session.refresh(db_task)

        return db_task