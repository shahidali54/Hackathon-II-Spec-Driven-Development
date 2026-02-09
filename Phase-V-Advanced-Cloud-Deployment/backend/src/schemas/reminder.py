from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class ReminderBase(BaseModel):
    task_id: uuid.UUID
    remind_at: datetime
    sent: bool = False

class ReminderCreate(ReminderBase):
    pass

class ReminderUpdate(BaseModel):
    task_id: Optional[uuid.UUID] = None
    remind_at: Optional[datetime] = None
    sent: Optional[bool] = None

class ReminderRead(ReminderBase):
    id: uuid.UUID
    sent_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime