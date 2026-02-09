from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
from pydantic import validator

class ReminderBase(SQLModel):
    task_id: uuid.UUID = Field(foreign_key="task.id")
    remind_at: datetime = Field(sa_column_kwargs={"nullable": False})
    sent: bool = Field(default=False)

    @validator('remind_at')
    def remind_at_must_be_future(cls, v):
        if v < datetime.utcnow():
            raise ValueError('Reminder time must be in the future')
        return v

class Reminder(ReminderBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    sent_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ReminderCreate(ReminderBase):
    pass

class ReminderRead(ReminderBase):
    id: uuid.UUID
    sent_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime