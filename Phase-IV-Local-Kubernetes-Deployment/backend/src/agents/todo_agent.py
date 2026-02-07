import os
from openai import AsyncOpenAI
from openai.lib.azure import AzureOpenAI
from ..tools.task_tools import TaskTools, CreateTaskParams, GetTasksParams, UpdateTaskParams, DeleteTaskParams, ToggleTaskCompletionParams
from pydantic import BaseModel
from typing import List, Optional
import json


class TodoAgent:
    """
    AI Agent for todo management using the OpenAI Functions API.
    The agent can perform task Create, Read, Update, and Delete operations
    by calling the existing backend task APIs through function calling.
    """

    def __init__(self):
        # Initialize the task tools that the agent will use
        self.task_tools = TaskTools()

        from dotenv import load_dotenv
        load_dotenv()

        # Initialize OpenAI client with API key from environment
        self.openai_client = AsyncOpenAI(api_key=os.getenv("OpenAI_API_KEY"))

        # Define the available functions/tools
        self.functions = [
            {
                "name": "create_task",
                "description": "Create a new task with the given title and optional description",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "The title of the task"},
                        "description": {"type": "string", "description": "The description of the task (optional)"}
                    },
                    "required": ["title"]
                }
            },
            {
                "name": "get_tasks",
                "description": "Get tasks for the current user. Optionally filter by completion status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "completed": {"type": "boolean", "description": "Filter by completion status (optional)"}
                    }
                }
            },
            {
                "name": "update_task",
                "description": "Update an existing task with the given ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to update"},
                        "title": {"type": "string", "description": "The new title of the task (optional)"},
                        "description": {"type": "string", "description": "The new description of the task (optional)"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "delete_task",
                "description": "Delete a task with the given ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to delete"}
                    },
                    "required": ["task_id"]
                }
            },
            {
                "name": "toggle_task_completion",
                "description": "Toggle the completion status of a task with the given ID",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "task_id": {"type": "string", "description": "The ID of the task to update"},
                        "completed": {"type": "boolean", "description": "The new completion status"}
                    },
                    "required": ["task_id", "completed"]
                }
            }
        ]

    def get_agent(self):
        """
        Return the function definitions for the agent.
        """
        return self.functions

    async def run_agent(self, user_input: str):
        """
        Run the agent with the given user input.
        """
        try:
            # Call the OpenAI API with function calling
            response = await self.openai_client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        You are a helpful todo management assistant. Help users manage their tasks by creating, reading, updating, and deleting tasks.
                        Always be polite and confirm actions with the user before performing them when appropriate.
                        When a user asks to add a task, call the create_task function.
                        When a user asks to see their tasks, call the get_tasks function.
                        When a user asks to update a task, call the update_task function.
                        When a user asks to delete a task, call the delete_task function.
                        When a user asks to mark a task as complete/incomplete, call the toggle_task_completion function.
                        Always respond in a friendly and helpful manner.
                        """
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                functions=self.functions,
                function_call="auto"
            )

            # Process the response
            message = response.choices[0].message

            if message.function_call:
                # If a function was called, return the function call
                function_call = message.function_call
                return {
                    "type": "function_call",
                    "name": function_call.name,
                    "arguments": json.loads(function_call.arguments)
                }
            else:
                # If no function was called, return the message content
                return {
                    "type": "message",
                    "content": message.content
                }

        except Exception as e:
            return {
                "type": "error",
                "content": f"Error running agent: {str(e)}"
            }