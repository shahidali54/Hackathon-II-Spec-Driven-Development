from sqlmodel import SQLModel
from src.database.database import engine
from src.models.user import User
from src.models.task import Task

def recreate_tables():
    print("Dropping and recreating database tables...")

    # Drop all tables first
    SQLModel.metadata.drop_all(bind=engine)
    print("Existing tables dropped.")

    # Create all tables
    SQLModel.metadata.create_all(bind=engine)
    print("Tables recreated successfully!")

if __name__ == "__main__":
    recreate_tables()