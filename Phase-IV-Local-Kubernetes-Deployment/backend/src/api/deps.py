from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlmodel import Session, select
from typing import Optional
from ..database.database import engine
from ..models.user import User
from ..utils.security import verify_token, get_user_id_from_token


def get_session():
    with Session(engine) as session:
        yield session
        # Session will be properly closed in finally block
        # The connection pooling settings in database.py handle reconnection

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db_session: Session = Depends(get_session)
) -> User:
    """Dependency to get the current user from the JWT token."""
    token = credentials.credentials
    print(f"DEBUG: Received token: {token[:30] if token else 'None'}...")  # Debug print

    # Verify the token and get user ID
    user_id = get_user_id_from_token(token)
    print(f"DEBUG: Extracted user_id: {user_id}")  # Debug print

    if user_id is None:
        print(f"DEBUG: Invalid token received: {token[:20] if token else 'None'}...")  # Debug print
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get the user from the database
    from sqlmodel import select
    statement = select(User).where(User.id == user_id)
    user = db_session.exec(statement).first()

    if user is None:
        print(f"DEBUG: User not found for ID: {user_id}")  # Debug print
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    print(f"DEBUG: Successfully authenticated user: {user.email if user else 'Unknown'}")  # Debug print
    return user

def get_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Dependency to get the token payload without database lookup."""
    token = credentials.credentials

    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload