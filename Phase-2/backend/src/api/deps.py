from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlmodel import Session
from typing import Optional
from ..database.database import engine
from ..models.user import User
from ..utils.security import verify_token, get_user_id_from_token


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db_session: Session = Depends(get_session)
) -> User:
    """Dependency to get the current user from the JWT token."""
    token = credentials.credentials

    # Verify the token and get user ID
    user_id = get_user_id_from_token(token)

    if user_id is None:
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

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