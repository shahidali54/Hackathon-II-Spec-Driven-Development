from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import auth, tasks
from src.api.chat import router as chat_router
from src.api.conversations import router as conversations_router
from src.api.conversation_messages import router as conversation_messages_router
from src.database.database import engine
from sqlmodel import SQLModel
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    SQLModel.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Todo API",
    description="API for managing user tasks in the Todo Full-Stack Web Application",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(conversations_router, prefix="/api", tags=["conversations"])
app.include_router(conversation_messages_router, prefix="/api", tags=["conversation-messages"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)