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

# Async engine for PostgreSQL with proper connection pooling for Neon Serverless
async_engine = create_async_engine(
    DATABASE_URL_ASYNC,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    pool_timeout=30,
    echo=False
)

# Synchronous engine for SQLModel with proper connection pooling for Neon Serverless
engine = create_engine(
    DATABASE_URL_SYNC,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    pool_timeout=30,
    echo=False
)

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