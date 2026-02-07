from sqlmodel import Session
from src.database.database import engine
from src.models.user import UserCreate
from src.services.auth_service import AuthService
from src.utils.security import get_password_hash

def test_direct_registration():
    print("Testing direct user registration...")

    # Test the password hashing function directly
    try:
        hashed = get_password_hash("pass123")
        print(f"Password hashing works: {type(hashed)}")
    except Exception as e:
        print(f"Password hashing failed: {e}")
        return False

    # Create a test user
    user_create = UserCreate(
        email="testfinal@example.com",
        password="pass123"
    )

    # Create a database session
    with Session(engine) as session:
        auth_service = AuthService(session)

        try:
            # Attempt to create the user
            db_user = auth_service.create_user(user_create)
            print(f"User created successfully: {db_user.email}")

            # Now try to authenticate the user
            authenticated_user = auth_service.authenticate_user("testfinal@example.com", "pass123")
            if authenticated_user:
                print(f"User authenticated successfully: {authenticated_user.email}")

                # Try to create access token
                token_data = auth_service.create_access_token_for_user(authenticated_user)
                print(f"Access token created: {type(token_data.access_token)}")
                return True
            else:
                print("Authentication failed")
                return False
        except Exception as e:
            print(f"Error creating user: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    success = test_direct_registration()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")