from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.message import Message, MessageCreate, MessageUpdate
from datetime import datetime
import uuid
import json


class MessageService:
    def __init__(self, session: Session):
        self.session = session

    def create_message(self, message_data: MessageCreate) -> Message:
        # Convert dict to JSON string if message_metadata is a dict
        metadata_json = None
        if message_data.message_metadata and isinstance(message_data.message_metadata, dict):
            metadata_json = json.dumps(message_data.message_metadata)
        else:
            metadata_json = message_data.message_metadata

        db_message = Message(
            conversation_id=message_data.conversation_id,
            user_id=message_data.user_id,
            role=message_data.role,
            content=message_data.content,
            message_metadata=metadata_json
        )

        self.session.add(db_message)
        self.session.commit()
        self.session.refresh(db_message)
        return db_message

    def get_message_by_id(self, message_id: str) -> Optional[Message]:
        statement = select(Message).where(Message.id == UUID(message_id))
        return self.session.exec(statement).first()

    def get_messages_by_conversation(self, conversation_id: str, limit: Optional[int] = None, offset: Optional[int] = None) -> List[Message]:
        statement = select(Message).where(Message.conversation_id == UUID(conversation_id)).order_by(Message.timestamp.asc())

        if offset:
            statement = statement.offset(offset)
        if limit:
            statement = statement.limit(limit)

        return self.session.exec(statement).all()

    def get_messages_by_conversation_and_user(self, conversation_id: str, user_id: str) -> List[Message]:
        statement = select(Message).where(
            Message.conversation_id == UUID(conversation_id),
            Message.user_id == UUID(user_id)
        ).order_by(Message.timestamp.asc())
        return self.session.exec(statement).all()

    def update_message(self, message_id: str, message_update: MessageUpdate) -> Optional[Message]:
        db_message = self.get_message_by_id(message_id)
        if not db_message:
            return None

        update_data = message_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'message_metadata' and value and isinstance(value, dict):
                setattr(db_message, field, json.dumps(value))
            else:
                setattr(db_message, field, value)

        self.session.add(db_message)
        self.session.commit()
        self.session.refresh(db_message)
        return db_message

    def delete_message(self, message_id: str) -> bool:
        db_message = self.get_message_by_id(message_id)
        if not db_message:
            return False

        self.session.delete(db_message)
        self.session.commit()
        return True