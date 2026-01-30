from typing import List, Optional
from pydantic import BaseModel
import httpx
import os
from ..models.task import TaskRead


# Pydantic models for tool parameters
class CreateTaskParams(BaseModel):
    title: str
    description: Optional[str] = None


class GetTasksParams(BaseModel):
    completed: Optional[bool] = None


class UpdateTaskParams(BaseModel):
    task_id: str
    title: Optional[str] = None
    description: Optional[str] = None


class DeleteTaskParams(BaseModel):
    task_id: str


class ToggleTaskCompletionParams(BaseModel):
    task_id: str
    completed: bool


class TaskTools:
    """
    MCP tools for task operations that the AI agent can use.
    These tools call the existing backend task APIs with proper authentication.
    """

    def __init__(self, base_url: str = None, api_key: str = None):
        self.base_url = base_url or os.getenv("TASK_API_BASE_URL", "http://localhost:8000/api")
        self.api_key = api_key or os.getenv("TASK_API_KEY")

    async def create_task(self, params: CreateTaskParams, user_token: str) -> TaskRead:
        """
        Create a new task via the existing task API.
        """
        headers = {
            "Authorization": f"Bearer {user_token}",
            "Content-Type": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/tasks",
                json={"title": params.title, "description": params.description},
                headers=headers
            )
            response.raise_for_status()
            return TaskRead(**response.json())

    async def get_tasks(self, params: GetTasksParams, user_token: str) -> List[TaskRead]:
        """
        Get tasks for the authenticated user via the existing task API.
        """
        headers = {
            "Authorization": f"Bearer {user_token}"
        }

        url = f"{self.base_url}/tasks"
        params_dict = {}
        if params.completed is not None:
            params_dict["completed"] = params.completed

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=params_dict)
            response.raise_for_status()
            tasks_data = response.json()
            return [TaskRead(**task_data) for task_data in tasks_data]

    async def update_task(self, params: UpdateTaskParams, user_token: str) -> TaskRead:
        """
        Update a task via the existing task API.
        """
        headers = {
            "Authorization": f"Bearer {user_token}",
            "Content-Type": "application/json"
        }

        update_data = {}
        if params.title is not None:
            update_data["title"] = params.title
        if params.description is not None:
            update_data["description"] = params.description

        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}/tasks/{params.task_id}",
                json=update_data,
                headers=headers
            )
            response.raise_for_status()
            return TaskRead(**response.json())

    async def delete_task(self, params: DeleteTaskParams, user_token: str) -> bool:
        """
        Delete a task via the existing task API.
        """
        headers = {
            "Authorization": f"Bearer {user_token}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/tasks/{params.task_id}",
                headers=headers
            )
            response.raise_for_status()
            return response.status_code == 200

    async def toggle_task_completion(self, params: ToggleTaskCompletionParams, user_token: str) -> TaskRead:
        """
        Toggle task completion status via the existing task API.
        """
        headers = {
            "Authorization": f"Bearer {user_token}"
        }

        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{self.base_url}/tasks/{params.task_id}/complete",
                params={"completed": params.completed},
                headers=headers
            )
            response.raise_for_status()
            return TaskRead(**response.json())