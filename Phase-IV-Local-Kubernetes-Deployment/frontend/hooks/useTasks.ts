"use client";

import { useState, useEffect, useCallback } from "react";
import type { Task, TaskCreateData, TaskUpdateData, TasksState } from "@/types";
import { ApiError, taskApi } from "@/lib/api-client";
import { useAuth } from "@/hooks/useAuth";

interface UseTasksReturn extends TasksState {
  fetchTasks: () => Promise<void>;
  createTask: (data: TaskCreateData) => Promise<Task>;
  updateTask: (id: number, data: TaskUpdateData) => Promise<Task>;
  deleteTask: (id: number) => Promise<void>;
  toggleComplete: (id: number) => Promise<Task>;
  setFilter: (isCompleted: boolean | null) => void;
  clearError: () => void;
}

export function useTasks(): UseTasksReturn {
  const [state, setState] = useState<TasksState>({
    items: [],
    total: 0,
    isLoading: false,
    error: null,
    filter: { isCompleted: null },
    pagination: { limit: 100, offset: 0 },
  });

  const { isAuthenticated, isLoading: authLoading } = useAuth();

  const fetchTasks = useCallback(async () => {
    setState((p) => ({ ...p, isLoading: true, error: null }));

    try {
      const tasks = await taskApi.getTasks({
        is_completed: state.filter.isCompleted ?? undefined,
        limit: state.pagination.limit,
        offset: state.pagination.offset,
      });

      setState((p) => ({
        ...p,
        items: tasks,
        total: tasks.length,
        isLoading: false,
        error: null,
      }));
    } catch (e) {
      setState((p) => ({
        ...p,
        isLoading: false,
        error:
          e instanceof ApiError ? e.message : "Failed to load tasks",
      }));
    }
  }, [
    state.filter.isCompleted,
    state.pagination.limit,
    state.pagination.offset,
  ]);

  useEffect(() => {
    if (!authLoading && isAuthenticated) {
      fetchTasks();
    }
  }, [fetchTasks, authLoading, isAuthenticated]);

  const createTask = useCallback(async (data: TaskCreateData) => {
    setState((p) => ({ ...p, isLoading: true, error: null }));

    try {
      const task = await taskApi.createTask(data);
      setState((p) => ({
        ...p,
        items: [task, ...p.items],
        total: p.total + 1,
        isLoading: false,
        error: null,
      }));
      return task;
    } catch (e) {
      setState((p) => ({
        ...p,
        isLoading: false,
        error:
          e instanceof ApiError ? e.message : "Create failed",
      }));
      throw e;
    }
  }, []);

  const updateTask = useCallback(async (id: number, data: TaskUpdateData) => {
    const updated = await taskApi.updateTask(id, data);
    setState((p) => ({
      ...p,
      items: p.items.map((t) => (t.id === id ? updated : t)),
      error: null,
    }));
    return updated;
  }, []);

  const deleteTask = useCallback(async (id: number) => {
    await taskApi.deleteTask(id);
    setState((p) => ({
      ...p,
      items: p.items.filter((t) => t.id !== id),
      total: p.total - 1,
      error: null,
    }));
  }, []);

  const toggleComplete = useCallback(
    async (id: number) => {
      const task = state.items.find((t) => t.id === id);
      if (!task) throw new Error("Task not found");

      const updated = await taskApi.toggleComplete(
        id,
        !task.is_completed
      );

      setState((p) => ({
        ...p,
        items: p.items.map((t) =>
          t.id === id ? updated : t
        ),
        error: null,
      }));

      return updated;
    },
    [state.items]
  );

  const setFilter = useCallback((isCompleted: boolean | null) => {
    setState((p) => ({
      ...p,
      filter: { isCompleted },
      pagination: { ...p.pagination, offset: 0 },
      error: null,
    }));
  }, []);

  const clearError = useCallback(() => {
    setState((p) => ({ ...p, error: null }));
  }, []);

  return {
    ...state,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleComplete,
    setFilter,
    clearError,
  };
}
