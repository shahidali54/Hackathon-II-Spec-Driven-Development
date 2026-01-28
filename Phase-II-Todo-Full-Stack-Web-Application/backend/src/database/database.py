from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL_ASYNC = os.getenv("DATABASE_URL", "postgresql+asyncpg://username:password@localhost/todo_db")
DATABASE_URL_SYNC = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/todo_db").replace("postgresql+asyncpg://", "postgresql://")

# Async engine for PostgreSQL
async_engine = create_async_engine(DATABASE_URL_ASYNC)

# Synchronous engine for SQLModel (needed for table creation)
engine = create_engine(DATABASE_URL_SYNC)

# Async session maker
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency to get async session
async def get_async_session():
    async with AsyncSessionLocal() as session:
        yield session