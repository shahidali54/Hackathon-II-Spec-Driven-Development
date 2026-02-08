from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from ..models.conversation import Conversation, ConversationCreate, ConversationUpdate
from datetime import datetime
import uuid


class ConversationService:
    def __init__(self, session: Session):
        self.session = session

    def create_conversation(self, conversation_data: ConversationCreate, user_id: str) -> Conversation:
        # Auto-generate title from first message if not provided
        title = conversation_data.title
        if not title:
            title = "New Conversation"

        db_conversation = Conversation(
            title=title,
            user_id=UUID(user_id)
        )

        self.session.add(db_conversation)
        self.session.commit()
        self.session.refresh(db_conversation)
        return db_conversation

    def get_conversation_by_id_and_user(self, conversation_id: str, user_id: str) -> Optional[Conversation]:
        statement = select(Conversation).where(
            Conversation.id == UUID(conversation_id),
            Conversation.user_id == UUID(user_id)
        )
        return self.session.exec(statement).first()

    def get_conversations_by_user(self, user_id: str) -> List[Conversation]:
        statement = select(Conversation).where(Conversation.user_id == UUID(user_id)).order_by(Conversation.created_at.desc())
        return self.session.exec(statement).all()

    def update_conversation(self, conversation_id: str, conversation_update: ConversationUpdate, user_id: str) -> Optional[Conversation]:
        db_conversation = self.get_conversation_by_id_and_user(conversation_id, user_id)
        if not db_conversation:
            return None

        update_data = conversation_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_conversation, field, value)

        db_conversation.updated_at = datetime.utcnow()

        self.session.add(db_conversation)
        self.session.commit()
        self.session.refresh(db_conversation)
        return db_conversation

    def delete_conversation(self, conversation_id: str, user_id: str) -> bool:
        db_conversation = self.get_conversation_by_id_and_user(conversation_id, user_id)
        if not db_conversation:
            return False

        self.session.delete(db_conversation)
        self.session.commit()
        return True