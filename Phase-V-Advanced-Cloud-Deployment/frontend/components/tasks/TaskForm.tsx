"use client";

import { useForm, Controller } from "react-hook-form";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import type { TaskFormData } from "@/types";
import { useState } from "react";

interface TaskFormProps {
  initialData?: TaskFormData;
  onSubmit: (data: TaskFormData) => Promise<void>;
  onCancel: () => void;
  isSubmitting: boolean;
  submitLabel?: string;
}

const PRIORITY_OPTIONS = [
  { value: "low", label: "Low Priority", icon: "⬇️", description: "Can wait", color: "bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800 text-green-700 dark:text-green-300" },
  { value: "medium", label: "Medium Priority", icon: "→", description: "Normal pace", color: "bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800 text-yellow-700 dark:text-yellow-300" },
  { value: "high", label: "High Priority", icon: "⬆️", description: "Soon needed", color: "bg-orange-50 dark:bg-orange-900/20 border-orange-200 dark:border-orange-800 text-orange-700 dark:text-orange-300" },
  { value: "urgent", label: "Urgent", icon: "🔥", description: "Do it now", color: "bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800 text-red-700 dark:text-red-300" },
];

const RECURRENCE_OPTIONS = [
  { value: "daily", label: "Daily", icon: "🔄" },
  { value: "weekly", label: "Weekly", icon: "📅" },
  { value: "monthly", label: "Monthly", icon: "🗓️" },
  { value: "yearly", label: "Yearly", icon: "📆" },
];

export function TaskForm({
  initialData,
  onSubmit,
  onCancel,
  isSubmitting,
  submitLabel = "Create Task",
}: TaskFormProps) {
  const {
    register,
    handleSubmit,
    control,
    watch,
    formState: { errors },
  } = useForm<TaskFormData>({
    defaultValues: initialData || {
      title: "",
      description: "",
      priority: "medium",
      tags: [],
      due_date: "",
      recurrence_rule: {
        enabled: false,
        frequency: "daily",
        interval: 1,
      },
    },
  });

  const [tagInput, setTagInput] = useState("");
  const watchedTags = watch("tags") as string[];
  const watchedRecurrence = watch("recurrence_rule");

  const handleAddTag = () => {
    if (tagInput.trim() && !watchedTags.includes(tagInput.trim())) {
      const newTags = [...(watchedTags || []), tagInput.trim()];
      register("tags").onChange({ target: { value: newTags } });
      setTagInput("");
    }
  };

  const handleRemoveTag = (tag: string) => {
    const newTags = (watchedTags || []).filter((t) => t !== tag);
    register("tags").onChange({ target: { value: newTags } });
  };

  const handleFormSubmit = async (data: TaskFormData) => {
    await onSubmit(data);
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="w-full h-full flex flex-col min-w-0">
      {/* Header */}
      <div className="flex-shrink-0 pb-2 md:pb-3 border-b border-zinc-200 dark:border-zinc-700">
        <h2 className="text-lg md:text-xl font-bold text-zinc-900 dark:text-white flex items-center gap-1.5">
          <span className="text-xl md:text-2xl flex-shrink-0">✨</span>
          <span className="truncate">{submitLabel === "Update Task" ? "Edit Task" : "Create New Task"}</span>
        </h2>
      </div>

      {/* Scrollable Content */}
      <div className="flex-1 overflow-y-auto min-h-0 w-full">
        <div className="p-3 md:p-4 space-y-3 md:space-y-4 w-full min-w-0">
          {/* Title Section */}
          <div className="space-y-1">
            <label className="block text-xs md:text-sm font-semibold text-zinc-700 dark:text-zinc-300 flex items-center gap-1">
              <span>📝</span>
              Title <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              placeholder="e.g., Complete project proposal"
              disabled={isSubmitting}
              className="w-full px-2 md:px-3 py-1.5 md:py-2 border-2 border-zinc-300 dark:border-zinc-600 rounded text-xs md:text-sm bg-white dark:bg-zinc-900 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/30 disabled:bg-zinc-100 dark:disabled:bg-zinc-800"
              {...register("title", {
                required: "Title is required",
                minLength: { value: 1, message: "Title cannot be empty" },
                maxLength: { value: 255, message: "Title too long" },
                validate: (value) =>
                  value.trim().length > 0 || "Title cannot be only whitespace",
              })}
            />
            {errors.title && (
              <p className="text-xs text-red-500 dark:text-red-400 flex items-center gap-1">
                <span>⚠️</span>
                {errors.title.message}
              </p>
            )}
          </div>

          {/* Description Section */}
          <div className="space-y-1">
            <label className="block text-xs md:text-sm font-semibold text-zinc-700 dark:text-zinc-300 flex items-center gap-1">
              <span>📋</span>
              Description
            </label>
            <textarea
              rows={2}
              placeholder="Add details... (optional)"
              disabled={isSubmitting}
              className="w-full px-2 md:px-3 py-1.5 md:py-2 border-2 border-zinc-300 dark:border-zinc-600 rounded text-xs md:text-sm bg-white dark:bg-zinc-900 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/30 disabled:bg-zinc-100 dark:disabled:bg-zinc-800 resize-none"
              {...register("description", {
                maxLength: { value: 1000, message: "Description too long" },
              })}
            />
            {errors.description && (
              <p className="text-xs text-red-500 dark:text-red-400">⚠️ {errors.description.message}</p>
            )}
          </div>

          {/* Priority Section */}
          <div className="space-y-1.5">
            <label className="block text-xs md:text-sm font-semibold text-zinc-700 dark:text-zinc-300 flex items-center gap-1">
              <span>⭐</span>
              Priority
            </label>
            <div className="grid grid-cols-2 gap-1.5">
              {PRIORITY_OPTIONS.map((option) => (
                <label
                  key={option.value}
                  className={`relative flex items-center p-1.5 md:p-2 rounded border-2 cursor-pointer transition-all text-xs md:text-sm ${
                    watch("priority") === option.value
                      ? `${option.color} border-current shadow-md`
                      : `border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 hover:border-zinc-400`
                  }`}
                >
                  <input
                    type="radio"
                    value={option.value}
                    {...register("priority")}
                    className="sr-only"
                  />
                  <div className="flex items-center gap-1 w-full min-w-0">
                    <span className="text-sm md:text-base flex-shrink-0">{option.icon}</span>
                    <div className="min-w-0 truncate">
                      <div className="font-semibold truncate">{option.label.split(" ")[0]}</div>
                    </div>
                  </div>
                </label>
              ))}
            </div>
          </div>

          {/* Due Date & Tags Row */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full min-w-0">
            {/* Due Date */}
            <div className="space-y-1 min-w-0">
              <label className="block text-xs md:text-sm font-semibold text-zinc-700 dark:text-zinc-300 flex items-center gap-1">
                <span>📆</span>
                Due Date
              </label>
              <input
                id="due_date"
                type="datetime-local"
                disabled={isSubmitting}
                className="w-full px-2 md:px-3 py-1.5 md:py-2 border-2 border-zinc-300 dark:border-zinc-600 rounded text-xs md:text-sm bg-white dark:bg-zinc-900 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/30 disabled:bg-zinc-100 dark:disabled:bg-zinc-800"
                {...register("due_date")}
              />
            </div>

            {/* Tags Input */}
            <div className="space-y-1 min-w-0">
              <label className="block text-xs md:text-sm font-semibold text-zinc-700 dark:text-zinc-300 flex items-center gap-1">
                <span>🏷️</span>
                Tags
              </label>
              <div className="flex gap-1">
                <input
                  type="text"
                  value={tagInput}
                  onChange={(e) => setTagInput(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      handleAddTag();
                    }
                  }}
                  placeholder="tag"
                  disabled={isSubmitting}
                  className="flex-1 px-2 md:px-3 py-1.5 md:py-2 border-2 border-zinc-300 dark:border-zinc-600 rounded text-xs md:text-sm bg-white dark:bg-zinc-900 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500/30 disabled:bg-zinc-100"
                />
                <Button
                  type="button"
                  variant="secondary"
                  onClick={handleAddTag}
                  disabled={isSubmitting || !tagInput.trim()}
                  className="px-2 md:px-3 py-1.5 md:py-2 text-xs"
                >
                  Add
                </Button>
              </div>
            </div>
          </div>

          {/* Tags Display */}
          {watchedTags && watchedTags.length > 0 && (
            <div className="flex flex-wrap gap-1 p-2 bg-blue-50 dark:bg-blue-900/20 rounded border border-blue-200 dark:border-blue-800 w-full min-w-0">
              {watchedTags.map((tag) => (
                <button
                  key={tag}
                  type="button"
                  onClick={() => handleRemoveTag(tag)}
                  className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-blue-500 dark:bg-blue-600 text-white hover:bg-blue-600 transition-colors"
                >
                  <span>#{tag}</span>
                  <span className="font-bold">×</span>
                </button>
              ))}
            </div>
          )}

          {/* Recurrence Section */}
          <div className="space-y-1.5 p-2 md:p-3 bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 rounded-lg border border-purple-200 dark:border-purple-800 w-full min-w-0">
            <div className="flex items-center gap-2">
              <input
                id="recurrence_enabled"
                type="checkbox"
                checked={watchedRecurrence?.enabled || false}
                onChange={(e) => {
                  const current = watch("recurrence_rule") || {};
                  register("recurrence_rule").onChange({
                    target: { value: { ...current, enabled: e.target.checked } },
                  });
                }}
                disabled={isSubmitting}
                className="w-3.5 h-3.5 md:w-4 md:h-4 text-purple-600 rounded cursor-pointer"
              />
              <label htmlFor="recurrence_enabled" className="text-xs md:text-sm font-semibold text-zinc-700 dark:text-zinc-300 cursor-pointer flex items-center gap-1">
                <span>🔄</span>
                Recurring
              </label>
            </div>

            {watchedRecurrence?.enabled && (
              <div className="grid grid-cols-2 gap-2 pt-2 border-t border-purple-200 dark:border-purple-800 w-full min-w-0">
                <div className="space-y-1 min-w-0">
                  <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300">Frequency</label>
                  <select
                    disabled={isSubmitting}
                    className="w-full px-2 py-1 border border-purple-300 dark:border-purple-700 rounded text-xs bg-white dark:bg-zinc-900 focus:outline-none focus:border-purple-500"
                    {...register("recurrence_rule.frequency")}
                  >
                    {RECURRENCE_OPTIONS.map((opt) => (
                      <option key={opt.value} value={opt.value}>
                        {opt.label}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="space-y-1 min-w-0">
                  <label className="block text-xs font-semibold text-zinc-700 dark:text-zinc-300">Interval</label>
                  <input
                    type="number"
                    min="1"
                    max="365"
                    disabled={isSubmitting}
                    className="w-full px-2 py-1 border border-purple-300 dark:border-purple-700 rounded text-xs bg-white dark:bg-zinc-900 focus:outline-none focus:border-purple-500"
                    {...register("recurrence_rule.interval", {
                      valueAsNumber: true,
                      min: { value: 1, message: "Min 1" },
                    })}
                  />
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Action Buttons - Fixed at Bottom */}
      <div className="flex-shrink-0 flex justify-end gap-2 p-3 md:p-4 border-t border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 w-full min-w-0">
        <Button
          type="button"
          variant="secondary"
          onClick={onCancel}
          disabled={isSubmitting}
          className="px-3 md:px-4 py-1.5 md:py-2 text-xs md:text-sm flex-shrink-0"
        >
          Cancel
        </Button>
        <Button
          type="submit"
          isLoading={isSubmitting}
          className="px-3 md:px-4 py-1.5 md:py-2 text-xs md:text-sm bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold flex-shrink-0"
        >
          {submitLabel === "Update Task" ? "Update" : "Create"}
        </Button>
      </div>
    </form>
  );
}
