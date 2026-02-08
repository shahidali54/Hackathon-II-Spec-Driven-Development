from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List
from uuid import UUID
from ..database.database import engine
from ..models.message import Message, MessageRead
from ..models.conversation import Conversation
from ..models.user import User
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService
from ..api.deps import get_current_user
from pydantic import BaseModel


class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    user_id: str
    role: str
    content: str
    timestamp: str
    message_metadata: dict


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


router = APIRouter()


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of messages to return"),
    offset: int = Query(0, ge=0, description="Number of messages to skip")
):
    """
    Get messages from a specific conversation for the authenticated user.
    """
    conversation_service = ConversationService(session)

    # Verify that the conversation belongs to the current user
    conversation = conversation_service.get_conversation_by_id_and_user(conversation_id, str(current_user.id))
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found or does not belong to user"
        )

    message_service = MessageService(session)
    messages = message_service.get_messages_by_conversation(conversation_id, limit=limit, offset=offset)

    # Convert to response format
    result = []
    for msg in messages:
        result.append(MessageResponse(
            id=str(msg.id),
            conversation_id=str(msg.conversation_id),
            user_id=str(msg.user_id),
            role=msg.role,
            content=msg.content,
            timestamp=msg.timestamp.isoformat(),
            message_metadata=msg.message_metadata or {}
        ))

    return result