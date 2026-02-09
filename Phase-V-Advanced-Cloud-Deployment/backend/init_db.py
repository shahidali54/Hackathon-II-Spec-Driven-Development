from sqlmodel import SQLModel
from src.database.database import engine
from src.models.user import User
from src.models.task import Task

def create_tables():
    print("Creating database tables...")

    # Import all models to ensure they're registered with SQLModel
    # Then create all tables
    SQLModel.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()