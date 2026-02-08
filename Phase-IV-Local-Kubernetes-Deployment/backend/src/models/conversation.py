from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class ConversationBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    user_id: uuid.UUID = Field(foreign_key="user.id", ondelete="CASCADE")


class Conversation(ConversationBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ConversationCreate(SQLModel):
    title: Optional[str] = None  # Allow auto-generation from first message


class ConversationRead(ConversationBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class ConversationUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)