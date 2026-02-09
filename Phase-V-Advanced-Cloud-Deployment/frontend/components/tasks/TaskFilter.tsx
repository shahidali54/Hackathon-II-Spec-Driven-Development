"use client";

import { cn } from "@/lib/utils";
import { useState } from "react";

interface TaskFilterProps {
  currentFilter: boolean | null;
  onFilterChange: (filter: boolean | null) => void;
  onPriorityChange?: (priority: string | null) => void;
  onTagsChange?: (tags: string[]) => void;
  availableTags?: string[];
}

const filters = [
  { label: "All", value: null },
  { label: "Active", value: false },
  { label: "Completed", value: true },
] as const;

const priorityFilters = [
  { label: "All Priorities", value: null },
  { label: "Low", value: "low" },
  { label: "Medium", value: "medium" },
  { label: "High", value: "high" },
  { label: "Urgent", value: "urgent" },
];

export function TaskFilter({
  currentFilter,
  onFilterChange,
  onPriorityChange,
  onTagsChange,
  availableTags = [],
}: TaskFilterProps) {
  const [selectedPriority, setSelectedPriority] = useState<string | null>(null);
  const [expandFilters, setExpandFilters] = useState(false);

  const handlePriorityChange = (priority: string | null) => {
    setSelectedPriority(priority);
    onPriorityChange?.(priority);
  };

  return (
    <div className="space-y-3 mb-6">
      {/* Completion Status Filter */}
      <div className="flex gap-2">
        {filters.map((filter) => (
          <button
            key={String(filter.value)}
            onClick={() => onFilterChange(filter.value)}
            className={cn(
              "px-3 py-1.5 text-sm font-medium rounded-lg transition-colors",
              currentFilter === filter.value
                ? "bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400"
                : "text-zinc-600 hover:bg-zinc-100 dark:text-zinc-400 dark:hover:bg-zinc-800"
            )}
          >
            {filter.label}
          </button>
        ))}
      </div>

      {/* Advanced Filters Toggle */}
      <button
        onClick={() => setExpandFilters(!expandFilters)}
        className="flex items-center gap-2 px-3 py-1.5 text-sm font-medium text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800 rounded-lg transition-colors"
      >
        <svg
          className={cn(
            "w-4 h-4 transition-transform",
            expandFilters && "rotate-180"
          )}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 14l-7 7m0 0l-7-7m7 7V3"
          />
        </svg>
        Advanced Filters
      </button>

      {/* Advanced Filters */}
      {expandFilters && (
        <div className="p-3 bg-zinc-50 dark:bg-zinc-800/50 rounded-lg space-y-3">
          {/* Priority Filter */}
          {onPriorityChange && (
            <div>
              <label className="block text-xs font-medium text-zinc-600 dark:text-zinc-400 mb-2">
                Priority
              </label>
              <div className="flex flex-wrap gap-2">
                {priorityFilters.map((prio) => (
                  <button
                    key={String(prio.value)}
                    onClick={() => handlePriorityChange(prio.value)}
                    className={cn(
                      "px-2 py-1 text-xs rounded transition-colors",
                      selectedPriority === prio.value
                        ? "bg-blue-200 dark:bg-blue-900/50 text-blue-700 dark:text-blue-300"
                        : "bg-white dark:bg-zinc-700 text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-600"
                    )}
                  >
                    {prio.label}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Tags Filter */}
          {onTagsChange && availableTags.length > 0 && (
            <div>
              <label className="block text-xs font-medium text-zinc-600 dark:text-zinc-400 mb-2">
                Tags
              </label>
              <div className="flex flex-wrap gap-2">
                {availableTags.map((tag) => (
                  <button
                    key={tag}
                    onClick={() => onTagsChange?.([tag])}
                    className="px-2 py-1 text-xs rounded bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 hover:bg-blue-200 dark:hover:bg-blue-900/50 transition-colors"
                  >
                    #{tag}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
