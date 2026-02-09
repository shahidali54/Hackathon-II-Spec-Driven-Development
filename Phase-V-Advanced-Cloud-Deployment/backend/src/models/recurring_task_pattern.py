from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from sqlalchemy import Column, JSON
from pydantic import validator

class RecurringTaskPatternBase(SQLModel):
    task_id: uuid.UUID = Field(foreign_key="task.id")
    rule: dict = Field(sa_column=Column(JSON))  # JSON object defining the recurrence pattern
    next_occurrence: Optional[datetime] = None

    @validator('rule')
    def validate_recurrence_rule(cls, v):
        # Basic validation for recurrence rule
        if not isinstance(v, dict):
            raise ValueError('Recurrence rule must be a dictionary')

        if 'frequency' not in v or v['frequency'] not in ['daily', 'weekly', 'monthly', 'yearly']:
            raise ValueError('Frequency must be one of: daily, weekly, monthly, yearly')

        if 'interval' not in v or not isinstance(v['interval'], int) or v['interval'] < 1:
            raise ValueError('Interval must be a positive integer')

        return v

class RecurringTaskPattern(RecurringTaskPatternBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class RecurringTaskPatternCreate(RecurringTaskPatternBase):
    pass

class RecurringTaskPatternRead(RecurringTaskPatternBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime