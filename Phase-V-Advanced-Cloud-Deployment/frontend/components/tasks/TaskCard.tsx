"use client";

import { useState } from "react";
import { Task } from "@/types";
import { cn, formatRelativeTime } from "@/lib/utils";

interface TaskCardProps {
  task: Task;
  onToggleComplete: (id: number) => Promise<void>;
  onEdit: (task: Task) => void;
  onDelete: (task: Task) => void;
}

const PRIORITY_COLORS = {
  low: "text-green-600 bg-green-50 dark:bg-green-900/20",
  medium: "text-yellow-600 bg-yellow-50 dark:bg-yellow-900/20",
  high: "text-orange-600 bg-orange-50 dark:bg-orange-900/20",
  urgent: "text-red-600 bg-red-50 dark:bg-red-900/20",
};

export function TaskCard({
  task,
  onToggleComplete,
  onEdit,
  onDelete,
}: TaskCardProps) {
  const [isToggling, setIsToggling] = useState(false);

  const handleToggle = async () => {
    setIsToggling(true);
    try {
      await onToggleComplete(typeof task.id === 'number' ? task.id : parseInt(task.id, 10));
    } finally {
      setIsToggling(false);
    }
  };

  const isOverdue = task.due_date && new Date(task.due_date) < new Date() && !task.is_completed;
  const isDueSoon = task.due_date && !isOverdue && new Date(task.due_date).getTime() - Date.now() < 86400000 && !task.is_completed; // 24 hours

  return (
    <div
      className={cn(
        "bg-white dark:bg-zinc-900 rounded-lg border p-4 transition-all",
        task.is_completed
          ? "border-zinc-200 dark:border-zinc-800 opacity-75"
          : "border-zinc-200 dark:border-zinc-700",
        isOverdue && "border-red-300 dark:border-red-700 bg-red-50/30 dark:bg-red-950/20"
      )}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <button
          onClick={handleToggle}
          disabled={isToggling}
          className={cn(
            "mt-0.5 flex-shrink-0 w-5 h-5 rounded border-2 transition-colors",
            "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2",
            task.is_completed
              ? "bg-blue-600 border-blue-600 dark:bg-blue-500 dark:border-blue-500"
              : "border-zinc-300 dark:border-zinc-600 hover:border-blue-400",
            isToggling && "opacity-50 cursor-wait"
          )}
          aria-label={task.is_completed ? "Mark as incomplete" : "Mark as complete"}
        >
          {task.is_completed && (
            <svg
              className="w-full h-full text-white"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={3}
                d="M5 13l4 4L19 7"
              />
            </svg>
          )}
        </button>

        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1">
              <h3
                className={cn(
                  "text-base font-medium",
                  task.is_completed
                    ? "text-zinc-500 dark:text-zinc-500 line-through"
                    : "text-zinc-900 dark:text-zinc-100"
                )}
              >
                {task.title}
              </h3>
              {task.description && (
                <p
                  className={cn(
                    "mt-1 text-sm",
                    task.is_completed
                      ? "text-zinc-400 dark:text-zinc-600"
                      : "text-zinc-600 dark:text-zinc-400"
                  )}
                >
                  {task.description}
                </p>
              )}
            </div>

            {/* Priority Badge */}
            {task.priority && (
              <span className={cn(
                "px-2 py-1 rounded text-xs font-medium whitespace-nowrap",
                PRIORITY_COLORS[task.priority as keyof typeof PRIORITY_COLORS] || PRIORITY_COLORS.medium
              )}>
                {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
              </span>
            )}
          </div>

          {/* Meta Information */}
          <div className="mt-2 flex flex-wrap items-center gap-2">
            {/* Due Date */}
            {task.due_date && (
              <div className={cn(
                "text-xs px-2 py-1 rounded",
                isOverdue
                  ? "bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300"
                  : isDueSoon
                  ? "bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300"
                  : "bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400"
              )}>
                {isOverdue && "⚠️ "}
                {isDueSoon && "📅 "}
                {new Date(task.due_date).toLocaleDateString()}
              </div>
            )}

            {/* Tags */}
            {task.tags && task.tags.length > 0 && (
              <div className="flex gap-1 flex-wrap">
                {task.tags.map((tag) => (
                  <span
                    key={tag}
                    className="inline-flex items-center px-2 py-1 rounded text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300"
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            )}

            {/* Recurring Indicator */}
            {task.recurrence_rule && Object.keys(task.recurrence_rule).length > 0 && (
              <span className="text-xs px-2 py-1 rounded bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300">
                🔄 Recurring
              </span>
            )}
          </div>

          {/* Timestamp */}
          <p className="mt-2 text-xs text-zinc-400 dark:text-zinc-500">
            {formatRelativeTime(task.updated_at)}
          </p>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-1">
          <button
            onClick={() => onEdit(task)}
            className="p-2 text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300 transition-colors rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800"
            aria-label="Edit task"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-4 w-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
          </button>
          <button
            onClick={() => onDelete(task)}
            className="p-2 text-zinc-400 hover:text-red-600 dark:hover:text-red-400 transition-colors rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-800"
            aria-label="Delete task"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-4 w-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
