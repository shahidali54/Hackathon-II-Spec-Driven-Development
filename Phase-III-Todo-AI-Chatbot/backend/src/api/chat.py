from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Optional
from uuid import UUID
import uuid
from datetime import datetime
from ..database.database import engine
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message, MessageCreate
from ..models.user import User
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService
from ..api.deps import get_current_user
from ..agents.todo_agent import TodoAgent
from pydantic import BaseModel
import os


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    message_id: str


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


def format_conversation_history_for_agent(messages):
    """
    Format conversation history to provide context to the AI agent.
    """
    formatted_history = []
    for msg in messages:
        role_prefix = "User" if msg.role == "user" else "Assistant"
        formatted_history.append(f"{role_prefix}: {msg.content}")
    return "\n".join(formatted_history)


router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Main chat endpoint that processes user messages through the AI agent.
    Implements stateless operation with conversation context reconstruction from database.
    """
    # Initialize services
    conversation_service = ConversationService(session)
    message_service = MessageService(session)

    # Get or create conversation
    conversation_id = chat_request.conversation_id
    if conversation_id:
        # Validate that the conversation belongs to the current user
        conversation = conversation_service.get_conversation_by_id_and_user(conversation_id, str(current_user.id))
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or does not belong to user"
            )

        # Load conversation context by retrieving recent messages
        conversation_history = message_service.get_messages_by_conversation(conversation_id, limit=20)
    else:
        # Create a new conversation with auto-generated title
        title = f"Chat: {chat_request.message[:50]}..." if len(chat_request.message) > 50 else f"Chat: {chat_request.message}"
        conversation_data = ConversationCreate(title=title)
        conversation = conversation_service.create_conversation(conversation_data, str(current_user.id))
        conversation_id = str(conversation.id)

        # For new conversations, there's no history yet
        conversation_history = []

    # Save user's message
    user_message = MessageCreate(
        conversation_id=UUID(conversation_id),
        user_id=current_user.id,
        role="user",
        content=chat_request.message
    )
    user_db_message = message_service.create_message(user_message)

    # Format the conversation history for the AI agent
    if conversation_history:
        context_history = format_conversation_history_for_agent(conversation_history)
        # Prepare the full input for the agent including context
        full_input = f"Previous conversation:\n{context_history}\n\nCurrent user message: {chat_request.message}"
    else:
        # For new conversations, just use the current message
        full_input = f"Current user message: {chat_request.message}"

    # Initialize the AI agent
    todo_agent = TodoAgent()

    # Run the agent with the formatted input
    try:
        result = await todo_agent.run_agent(full_input)

        if result["type"] == "message":
            ai_response = result["content"]
        elif result["type"] == "function_call":
            # Handle function call by executing the actual task operation
            function_name = result["name"]
            function_args = result["arguments"]

            # Execute the actual function based on the function name
            if function_name == "create_task":
                # Create a task using the message service
                from ..models.task import TaskCreate
                task_create_data = TaskCreate(
                    title=function_args.get("title", "Untitled Task"),
                    description=function_args.get("description", "")
                )

                # Import and use the task service to create the task
                from ..services.task_service import TaskService
                task_service = TaskService(session)
                created_task = task_service.create_task(task_create_data, str(current_user.id))

                ai_response = f"I've created a task titled '{created_task.title}' for you!"
            elif function_name == "get_tasks":
                # Retrieve tasks using the task service
                from ..services.task_service import TaskService
                task_service = TaskService(session)
                completed_filter = function_args.get("completed")
                tasks = task_service.get_tasks_by_user(str(current_user.id), completed_filter)

                if tasks:
                    task_titles = [task.title for task in tasks]
                    ai_response = f"Here are your tasks: {', '.join(task_titles)}"
                else:
                    ai_response = "You don't have any tasks at the moment."
            elif function_name == "update_task":
                # Update a task using the task service
                from ..services.task_service import TaskService
                task_service = TaskService(session)

                task_id = function_args.get("task_id")
                title = function_args.get("title")
                description = function_args.get("description")

                # Prepare update data
                from ..models.task import TaskUpdate
                update_data = TaskUpdate(title=title, description=description)

                updated_task = task_service.update_task(task_id, update_data, str(current_user.id))
                if updated_task:
                    ai_response = f"I've updated the task titled '{updated_task.title}'."
                else:
                    ai_response = "I couldn't find that task to update."
            elif function_name == "delete_task":
                # Delete a task using the task service
                from ..services.task_service import TaskService
                task_service = TaskService(session)

                task_id = function_args.get("task_id")
                success = task_service.delete_task(task_id, str(current_user.id))

                if success:
                    ai_response = "I've deleted the task for you."
                else:
                    ai_response = "I couldn't find that task to delete."
            elif function_name == "toggle_task_completion":
                # Toggle task completion using the task service
                from ..services.task_service import TaskService
                task_service = TaskService(session)

                task_id = function_args.get("task_id")
                completed = function_args.get("completed", False)

                updated_task = task_service.toggle_task_completion(task_id, completed, str(current_user.id))
                if updated_task:
                    status = "completed" if updated_task.is_completed else "incomplete"
                    ai_response = f"I've marked the task '{updated_task.title}' as {status}."
                else:
                    ai_response = "I couldn't find that task to update."
            else:
                ai_response = f"Function call: {function_name} with arguments: {function_args}. Operation completed."
        elif result["type"] == "error":
            ai_response = f"Sorry, I encountered an error processing your request: {result['content']}"
        else:
            ai_response = "I processed your request but don't have a specific response to provide."
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message with AI agent: {str(e)}"
        )

    # Save AI's response
    ai_message = MessageCreate(
        conversation_id=UUID(conversation_id),
        user_id=current_user.id,
        role="assistant",
        content=ai_response
    )
    ai_db_message = message_service.create_message(ai_message)

    # Update conversation timestamp by updating the conversation with current time
    from ..models.conversation import ConversationUpdate
    conversation_update = ConversationUpdate(title=conversation.title)  # Just update timestamp by saving again
    updated_conversation = conversation_service.update_conversation(
        conversation_id,
        conversation_update,
        str(current_user.id)
    )

    return ChatResponse(
        response=ai_response,
        conversation_id=conversation_id,
        message_id=str(ai_db_message.id)
    )