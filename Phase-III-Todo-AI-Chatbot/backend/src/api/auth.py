from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, create_engine
from jose import jwt, JWTError
from datetime import timedelta
from ..database.database import engine
from ..models.user import User, UserCreate, UserRead, UserAuthData
from ..services.auth_service import AuthService


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()

router = APIRouter()
security = HTTPBearer()

@router.post("/auth/register", response_model=UserRead)
def register(user_create: UserCreate, session: Session = Depends(get_session)):
    auth_service = AuthService(session)
    try:
        db_user = auth_service.create_user(user_create)
        session.commit()  # Explicitly commit the transaction
        # Make sure all attributes are loaded before session closes
        _ = db_user.id  # Force loading of the user object
        return db_user
    except Exception as e:
        session.rollback()  # Rollback on error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed"
        )

@router.post("/auth/login", response_model=UserAuthData)
def login(email: str, password: str, session: Session = Depends(get_session)):
    auth_service = AuthService(session)
    user = auth_service.authenticate_user(email, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token using the auth service
    token_response = auth_service.create_access_token_for_user(user)

    return token_response

@router.post("/auth/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # In a real implementation, you might add the token to a blacklist
    # For now, we just return a success message
    return {"message": "Successfully logged out"}