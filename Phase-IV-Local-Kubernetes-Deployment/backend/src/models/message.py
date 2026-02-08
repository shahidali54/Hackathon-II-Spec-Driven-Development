from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid
import json


class MessageBase(SQLModel):
    conversation_id: uuid.UUID = Field(foreign_key="conversation.id", ondelete="CASCADE")
    user_id: uuid.UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    role: str = Field(regex="^(user|assistant)$")  # Either "user" or "assistant"
    content: str = Field(min_length=1, max_length=10000)  # Up to 10,000 characters
    message_metadata: Optional[str] = Field(default=None)  # JSON string for optional structured data


class Message(MessageBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class MessageCreate(MessageBase):
    pass


class MessageRead(MessageBase):
    id: uuid.UUID
    timestamp: datetime


class MessageUpdate(SQLModel):
    content: Optional[str] = Field(default=None, min_length=1, max_length=10000)
    message_metadata: Optional[str] = Field(default=None)