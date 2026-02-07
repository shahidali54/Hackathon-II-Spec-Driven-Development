from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List
from uuid import UUID
from ..database.database import engine
from ..models.conversation import Conversation, ConversationRead
from ..models.user import User
from ..services.conversation_service import ConversationService
from ..api.deps import get_current_user
from pydantic import BaseModel


class ConversationSummary(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


router = APIRouter()


@router.get("/conversations", response_model=List[ConversationSummary])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of conversations to return"),
    offset: int = Query(0, ge=0, description="Number of conversations to skip")
):
    """
    Get all conversations for the authenticated user.
    """
    conversation_service = ConversationService(session)
    conversations = conversation_service.get_conversations_by_user(str(current_user.id))

    # Apply pagination
    paginated_conversations = conversations[offset:offset+limit]

    # Convert to response format
    result = []
    for conv in paginated_conversations:
        result.append(ConversationSummary(
            id=str(conv.id),
            title=conv.title,
            created_at=conv.created_at.isoformat(),
            updated_at=conv.updated_at.isoformat()
        ))

    return result