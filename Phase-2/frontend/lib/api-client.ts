import {
  Task,
  TaskCreateData,
  TaskUpdateData,
  TaskQueryParams,
} from "@/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "https://shahidali1-separate-backend.hf.space/";

export class ApiError extends Error {
  public statusCode: number;
  public details: any;

  constructor(message: string, statusCode: number, details?: any) {
    super(message);
    this.name = "ApiError";
    this.statusCode = statusCode;
    this.details = details;
  }
}

async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem("auth_token");

  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let message = `HTTP ${response.status}`;
    try {
      const data = await response.json();
      message = data.detail || message;
    } catch {}
    throw new ApiError(message, response.status);
  }

  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}

export const taskApi = {
  getTasks: async (params?: TaskQueryParams): Promise<Task[]> => {
    const query = new URLSearchParams();

    if (params?.is_completed !== undefined) {
      query.append("completed", String(params.is_completed));
    }
    if (params?.limit !== undefined) {
      query.append("limit", String(params.limit));
    }
    if (params?.offset !== undefined) {
      query.append("offset", String(params.offset));
    }

    const qs = query.toString();
    return apiRequest<Task[]>(`/api/tasks${qs ? `?${qs}` : ""}`);
  },

  createTask: async (data: TaskCreateData): Promise<Task> => {
    return apiRequest<Task>("/api/tasks", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  updateTask: async (id: number, data: TaskUpdateData): Promise<Task> => {
    return apiRequest<Task>(`/api/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  },

  toggleComplete: async (id: number, completed: boolean): Promise<Task> => {
    return apiRequest<Task>(
      `/api/tasks/${id}/complete?completed=${completed}`,
      { method: "PATCH" }
    );
  },

  deleteTask: async (id: number): Promise<void> => {
    await apiRequest(`/api/tasks/${id}`, { method: "DELETE" });
  },
};
