from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class RecurringTaskPatternBase(BaseModel):
    task_id: uuid.UUID
    rule: dict
    next_occurrence: Optional[datetime] = None

class RecurringTaskPatternCreate(RecurringTaskPatternBase):
    pass

class RecurringTaskPatternUpdate(BaseModel):
    task_id: Optional[uuid.UUID] = None
    rule: Optional[dict] = None
    next_occurrence: Optional[datetime] = None

class RecurringTaskPatternRead(RecurringTaskPatternBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime