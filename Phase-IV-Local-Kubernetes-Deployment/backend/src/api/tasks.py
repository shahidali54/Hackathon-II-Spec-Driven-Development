from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from ..database.database import engine
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..models.user import User
from ..services.task_service import TaskService
from ..api.deps import get_current_user


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


router = APIRouter()

@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    completed: Optional[bool] = Query(None, description="Filter tasks by completion status"),
    limit: Optional[int] = Query(50, ge=1, le=100, description="Maximum number of tasks to return"),
    offset: Optional[int] = Query(0, ge=0, description="Number of tasks to skip"),
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.
    The user is identified from the JWT token.
    """

    task_service = TaskService(session)
    tasks = task_service.get_tasks_by_user(str(current_user.id), completed)

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

    task_service = TaskService(session)
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

    task_service = TaskService(session)
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

    task_service = TaskService(session)
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

    task_service = TaskService(session)
    updated_task = task_service.toggle_task_completion(id, completed, str(current_user.id))

    return updated_task