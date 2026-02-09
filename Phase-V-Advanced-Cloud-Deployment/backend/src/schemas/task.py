from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum
import uuid

class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    due_date: Optional[datetime] = None
    priority: PriorityEnum = PriorityEnum.medium
    tags: Optional[List[str]] = []
    recurrence_rule: Optional[dict] = {}
    reminder_sent: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[PriorityEnum] = None
    tags: Optional[List[str]] = None
    recurrence_rule: Optional[dict] = None
    reminder_sent: Optional[bool] = None

class TaskRead(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime