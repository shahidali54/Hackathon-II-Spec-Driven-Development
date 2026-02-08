from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import Optional
from datetime import timedelta
from ..models.user import User, UserCreate, UserAuthData
from ..utils.security import verify_password, get_password_hash, create_access_token, create_token_data

class AuthService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password."""
        statement = select(User).where(User.email == email)
        user = self.db_session.exec(statement).first()

        if not user or not verify_password(password, user.hashed_password):
            return None

        return user

    def create_user(self, user_create: UserCreate) -> User:
        """Create a new user with hashed password."""
        # Check if user already exists
        existing_user = self.db_session.exec(
            select(User).where(User.email == user_create.email)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash the password
        hashed_password = get_password_hash(user_create.password)

        # Create the user
        db_user = User(
            email=user_create.email,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            hashed_password=hashed_password
        )

        self.db_session.add(db_user)
        self.db_session.commit()
        self.db_session.refresh(db_user)

        return db_user

    def create_access_token_for_user(self, user: User) -> UserAuthData:
        """Create an access token for the given user."""
        token_data = create_token_data(str(user.id), user.email)
        access_token = create_access_token(
            data=token_data,
            expires_delta=timedelta(minutes=30)
        )

        return UserAuthData(access_token=access_token)

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        statement = select(User).where(User.email == email)
        user = self.db_session.exec(statement).first()
        return user