from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy import Column, ARRAY, String, JSON
from pydantic import field_validator
from enum import Enum
import json

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    is_completed: bool = Field(default=False)
    due_date: Optional[datetime] = None
    priority: str = Field(default="medium", sa_column=Column(String, default="medium"))  # Using string enum instead of int
    tags: Optional[list] = Field(default=[], sa_column=Column(ARRAY(String)))  # Array of tags
    recurrence_rule: Optional[dict] = Field(default={}, sa_column=Column(JSON))  # JSON for recurrence rule
    reminder_sent: bool = Field(default=False)  # Flag to track if reminder has been sent

    @field_validator('due_date')
    @classmethod
    def due_date_must_be_future_or_none(cls, v):
        # Allow None values
        if v is None:
            return v
        # Allow past dates (for editing tasks with past due dates)
        # but we could also validate that it's not in the far past
        return v

    @field_validator('priority')
    @classmethod
    def priority_must_be_valid(cls, v):
        if v not in ["low", "medium", "high", "urgent"]:
            raise ValueError('Priority must be one of: low, medium, high, urgent')
        return v

class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None  # Changed from Optional[int] to Optional[str] to match TaskBase
    tags: Optional[list] = None
    recurrence_rule: Optional[dict] = None
    reminder_sent: Optional[bool] = None