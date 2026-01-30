import asyncio
from sqlmodel import Session
from src.database.database import engine
from src.models.user import UserCreate
from src.services.auth_service import AuthService

def test_registration():
    print("Testing user registration...")

    # Create a test user
    user_create = UserCreate(
        email="test@example.com",
        password="pass123"
    )

    # Create a database session
    with Session(engine) as session:
        auth_service = AuthService(session)

        try:
            # Attempt to create the user
            db_user = auth_service.create_user(user_create)
            print(f"User created successfully: {db_user.email}")
            return db_user
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

if __name__ == "__main__":
    test_registration()