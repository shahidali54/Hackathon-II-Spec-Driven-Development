"use client";

import { useState, useEffect } from "react";
import { useTasks } from "@/hooks/useTasks";
import { TaskList } from "@/components/tasks/TaskList";
import { TaskForm } from "@/components/tasks/TaskForm";
import { TaskFilter } from "@/components/tasks/TaskFilter";
import { DeleteConfirm } from "@/components/tasks/DeleteConfirm";
import { Modal } from "@/components/ui/Modal";
import type { Task, TaskFormData } from "@/types";

export default function DashboardPage() {
  const {
    items: tasks,
    total,
    isLoading,
    error,
    filter,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    toggleComplete,
    setFilter,
  } = useTasks();

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deletingTask, setDeletingTask] = useState<Task | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [stats, setStats] = useState({
    completed: 0,
    pending: 0
  });
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    
    const completed = tasks.filter(task => task.is_completed).length;
    const pending = tasks.length - completed;
    
    setStats({ completed, pending });
  }, [tasks]);

  const handleCreate = async (data: TaskFormData) => {
    setIsSubmitting(true);
    try {
      await createTask({
        title: data.title,
        description: data.description || undefined,
      });
      setIsCreateModalOpen(false);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleEdit = async (data: TaskFormData) => {
    if (!editingTask) return;
    setIsSubmitting(true);
    try {
      await updateTask(editingTask.id, {
        title: data.title,
        description: data.description || undefined,
      });
      setEditingTask(null);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async () => {
    if (!deletingTask) return;
    setIsSubmitting(true);
    try {
      await deleteTask(deletingTask.id);
      setDeletingTask(null);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleToggleComplete = async (id: number) => {
    await toggleComplete(id);
  };

  if (!mounted) {
    return (
      <div className="min-h-screen w-full bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-950 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-950 overflow-x-hidden">
      <div className="fixed inset-0 overflow-hidden pointer-events-none w-full">
        <div className="absolute -top-20 -right-10 w-72 h-72 sm:-top-32 sm:-right-16 sm:w-96 sm:h-96 md:-top-40 md:-right-20 md:w-[500px] md:h-[500px] lg:-top-48 lg:-right-24 lg:w-[600px] lg:h-[600px] bg-blue-200/20 dark:bg-blue-500/10 rounded-full mix-blend-multiply blur-xl sm:blur-2xl md:blur-3xl animate-pulse"></div>
        <div className="absolute top-1/4 -left-8 w-64 h-64 sm:top-1/3 sm:-left-12 sm:w-80 sm:h-80 md:top-1/3 md:-left-16 md:w-96 md:h-96 lg:top-1/3 lg:-left-20 lg:w-[500px] lg:h-[500px] bg-purple-200/20 dark:bg-purple-500/10 rounded-full mix-blend-multiply blur-xl sm:blur-2xl md:blur-3xl animate-pulse delay-1000"></div>
      </div>

      <div className="w-full px-0 sm:px-1 md:px-2 lg:px-3 xl:px-4 2xl:px-6">
        <div className="mb-6 sm:mb-8 pt-4 sm:pt-6 w-full">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 sm:gap-6 mb-6 sm:mb-8 w-full">
            <div className="space-y-2 w-full">
              <div className="flex items-center gap-2 sm:gap-3 w-full">
                <div className="p-1.5 sm:p-2 rounded-lg sm:rounded-xl bg-gradient-to-br from-blue-600 to-purple-600 shadow-lg">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 sm:h-6 sm:w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 dark:from-white dark:to-gray-300 bg-clip-text text-transparent w-full">
                  Task Dashboard
                </h1>
              </div>
              <p className="text-sm sm:text-base md:text-lg text-gray-600 dark:text-gray-400 w-full">
                Manage your tasks efficiently and boost productivity
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 w-full sm:w-auto">
              <button
                onClick={() => setIsCreateModalOpen(true)}
                className="group relative px-4 py-2.5 sm:px-6 sm:py-3 md:px-8 md:py-3.5 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg sm:rounded-xl hover:shadow-xl sm:hover:shadow-2xl hover:shadow-blue-500/30 transition-all duration-300 hover:-translate-y-0.5 sm:hover:-translate-y-1 flex items-center justify-center gap-2 font-semibold w-full sm:w-auto text-sm sm:text-base md:text-lg"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 sm:h-5 sm:w-5 md:h-6 md:w-6 group-hover:rotate-90 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                <span className="hidden xs:inline">Create New Task</span>
                <span className="xs:hidden">New Task</span>
              </button>
              <a
                href="/dashboard/chat"
                className="group relative px-4 py-2.5 sm:px-6 sm:py-3 md:px-8 md:py-3.5 bg-gradient-to-r from-emerald-600 to-teal-600 text-white rounded-lg sm:rounded-xl hover:shadow-xl sm:hover:shadow-2xl hover:shadow-emerald-500/30 transition-all duration-300 hover:-translate-y-0.5 sm:hover:-translate-y-1 flex items-center justify-center gap-2 font-semibold w-full sm:w-auto text-sm sm:text-base md:text-lg"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 sm:h-5 sm:w-5 md:h-6 md:w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
                <span className="hidden xs:inline">AI Chat Assistant</span>
                <span className="xs:hidden">Chat</span>
              </a>
            </div>
          </div>

          <div className="grid grid-cols-1 xs:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-3 sm:gap-4 mb-6 sm:mb-8 w-full">
            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl sm:rounded-2xl p-4 sm:p-5 border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow w-full">
              <div className="flex items-center justify-between w-full">
                <div className="w-full">
                  <p className="text-xs sm:text-sm md:text-base text-gray-600 dark:text-gray-400 w-full">Total Tasks</p>
                  <p className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mt-0.5 sm:mt-1 w-full">{total}</p>
                </div>
                <div className="p-2 sm:p-3 md:p-4 rounded-lg sm:rounded-xl bg-blue-100 dark:bg-blue-900/30">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 sm:h-6 sm:w-6 md:h-7 md:w-7 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
              </div>
              <div className="mt-3 sm:mt-4 w-full">
                <div className="h-1.5 sm:h-2 md:h-2.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden w-full">
                  <div 
                    className="h-full bg-gradient-to-r from-blue-500 to-purple-500 rounded-full transition-all duration-500 w-full"
                    style={{ width: `${tasks.length > 0 ? (stats.completed / tasks.length) * 100 : 0}%` }}
                  ></div>
                </div>
                <div className="flex justify-between text-xs sm:text-sm md:text-base text-gray-500 dark:text-gray-400 mt-1.5 sm:mt-2 w-full">
                  <span>{stats.completed} completed</span>
                  <span>{stats.pending} pending</span>
                </div>
              </div>
            </div>

            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl sm:rounded-2xl p-4 sm:p-5 border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow w-full">
              <div className="flex items-center justify-between w-full">
                <div className="w-full">
                  <p className="text-xs sm:text-sm md:text-base text-gray-600 dark:text-gray-400 w-full">Completed</p>
                  <p className="text-2xl sm:text-3xl md:text-4xl font-bold text-green-600 dark:text-green-400 mt-0.5 sm:mt-1 w-full">{stats.completed}</p>
                </div>
                <div className="p-2 sm:p-3 md:p-4 rounded-lg sm:rounded-xl bg-green-100 dark:bg-green-900/30">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 sm:h-6 sm:w-6 md:h-7 md:w-7 text-green-600 dark:text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <div className="mt-3 sm:mt-4 w-full">
                <p className="text-xs sm:text-sm md:text-base text-gray-600 dark:text-gray-400 w-full">
                  {tasks.length > 0 ? Math.round((stats.completed / tasks.length) * 100) : 0}% of all tasks
                </p>
              </div>
            </div>

            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl sm:rounded-2xl p-4 sm:p-5 border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow xs:col-span-2 lg:col-span-1 w-full">
              <div className="flex items-center justify-between w-full">
                <div className="w-full">
                  <p className="text-xs sm:text-sm md:text-base text-gray-600 dark:text-gray-400 w-full">Pending</p>
                  <p className="text-2xl sm:text-3xl md:text-4xl font-bold text-amber-600 dark:text-amber-400 mt-0.5 sm:mt-1 w-full">{stats.pending}</p>
                </div>
                <div className="p-2 sm:p-3 md:p-4 rounded-lg sm:rounded-xl bg-amber-100 dark:bg-amber-900/30">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 sm:h-6 sm:w-6 md:h-7 md:w-7 text-amber-600 dark:text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <div className="mt-3 sm:mt-4 w-full">
                <p className="text-xs sm:text-sm md:text-base text-gray-600 dark:text-gray-400 w-full">
                  {tasks.length > 0 ? Math.round((stats.pending / tasks.length) * 100) : 0}% of all tasks
                </p>
              </div>
            </div>

            <div className="hidden xl:block bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl sm:rounded-2xl p-4 sm:p-5 border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow w-full">
              <div className="flex items-center justify-between w-full">
                <div className="w-full">
                  <p className="text-xs sm:text-sm md:text-base text-gray-600 dark:text-gray-400 w-full">Today's Progress</p>
                  <p className="text-2xl sm:text-3xl md:text-4xl font-bold text-purple-600 dark:text-purple-400 mt-0.5 sm:mt-1 w-full">
                    {tasks.length > 0 ? Math.round((stats.completed / tasks.length) * 100) : 0}%
                  </p>
                </div>
                <div className="p-2 sm:p-3 md:p-4 rounded-lg sm:rounded-xl bg-purple-100 dark:bg-purple-900/30">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 sm:h-6 sm:w-6 md:h-7 md:w-7 text-purple-600 dark:text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                </div>
              </div>
              <div className="mt-3 sm:mt-4 w-full">
                <p className="text-xs sm:text-sm md:text-base text-gray-600 dark:text-gray-400 w-full">
                  Daily completion rate
                </p>
              </div>
            </div>

            <div className="hidden 2xl:block bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl sm:rounded-2xl p-4 sm:p-5 border border-gray-200 dark:border-gray-700 shadow-sm hover:shadow-md transition-shadow w-full">
              <div className="flex items-center justify-between w-full">
                <div className="w-full">
                  <p className="text-xs sm:text-sm md:text-base text-gray-600 dark:text-gray-400 w-full">Active Streak</p>
                  <p className="text-2xl sm:text-3xl md:text-4xl font-bold text-pink-600 dark:text-pink-400 mt-0.5 sm:mt-1 w-full">7 days</p>
                </div>
                <div className="p-2 sm:p-3 md:p-4 rounded-lg sm:rounded-xl bg-pink-100 dark:bg-pink-900/30">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 sm:h-6 sm:w-6 md:h-7 md:w-7 text-pink-600 dark:text-pink-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
              </div>
              <div className="mt-3 sm:mt-4 w-full">
                <p className="text-xs sm:text-sm md:text-base text-gray-600 dark:text-gray-400 w-full">
                  Keep it up! 🔥
                </p>
              </div>
            </div>
          </div>
        </div>

        <div className="mb-4 sm:mb-6 w-full px-2 sm:px-3 md:px-4">
          <TaskFilter
            currentFilter={filter.isCompleted}
            onFilterChange={setFilter}
          />
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-4 2xl:grid-cols-5 gap-4 sm:gap-6 w-full px-2 sm:px-3 md:px-4">
          <div className="xl:col-span-3 2xl:col-span-4 w-full">
            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl sm:rounded-2xl border border-gray-200 dark:border-gray-700 shadow-sm overflow-hidden w-full">
              <div className="p-3 sm:p-4 md:p-5 border-b border-gray-200 dark:border-gray-700 w-full">
                <div className="flex flex-col xs:flex-row xs:items-center xs:justify-between gap-2 w-full">
                  <h2 className="text-lg sm:text-xl md:text-2xl font-semibold text-gray-900 dark:text-white w-full">
                    Your Tasks
                  </h2>
                  <div className="text-xs sm:text-sm md:text-base text-gray-600 dark:text-gray-400">
                    {tasks.length} of {total} shown
                  </div>
                </div>
              </div>

              {!isLoading && tasks.length === 0 && !error && (
                <div className="p-6 sm:p-8 md:p-12 lg:p-16 text-center w-full">
                  <div className="w-16 h-16 sm:w-20 sm:h-20 md:w-24 md:h-24 lg:w-32 lg:h-32 mx-auto mb-4 sm:mb-6 rounded-full bg-gradient-to-br from-gray-100 to-gray-200 dark:from-gray-800 dark:to-gray-900 flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 sm:h-10 sm:w-10 md:h-12 md:w-12 lg:h-16 lg:w-16 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                    </svg>
                  </div>
                  <h3 className="text-lg sm:text-xl md:text-2xl lg:text-3xl font-semibold text-gray-900 dark:text-white mb-2 w-full">
                    No tasks yet
                  </h3>
                  <p className="text-sm sm:text-base md:text-lg text-gray-600 dark:text-gray-400 mb-4 sm:mb-6 max-w-md mx-auto w-full">
                    Get started by creating your first task. Organize your work and boost your productivity.
                  </p>
                  <button
                    onClick={() => setIsCreateModalOpen(true)}
                    className="inline-flex items-center gap-2 px-4 py-2.5 sm:px-6 sm:py-3 md:px-8 md:py-3.5 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg sm:rounded-xl hover:shadow-lg transition-all duration-300 font-medium text-sm sm:text-base md:text-lg w-full sm:w-auto"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 sm:h-5 sm:w-5 md:h-6 md:w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                    </svg>
                    Create Your First Task
                  </button>
                </div>
              )}

              <div className="divide-y divide-gray-200 dark:divide-gray-700 w-full">
                <TaskList
                  tasks={tasks}
                  isLoading={isLoading}
                  error={error}
                  onToggleComplete={handleToggleComplete}
                  onEdit={setEditingTask}
                  onDelete={setDeletingTask}
                  onRetry={fetchTasks}
                />
              </div>
            </div>
          </div>

          <div className="space-y-4 sm:space-y-6 xl:col-span-1 w-full">
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 rounded-xl sm:rounded-2xl border border-blue-100 dark:border-blue-800/30 p-4 sm:p-5 w-full">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-3 sm:mb-4 flex items-center gap-2 text-sm sm:text-base md:text-lg w-full">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 sm:h-5 sm:w-5 md:h-6 md:w-6 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Productivity Tips
              </h3>
              <div className="space-y-3 sm:space-y-4 w-full">
                <div className="flex items-start gap-2 sm:gap-3 w-full">
                  <div className="w-6 h-6 sm:w-8 sm:h-8 md:w-10 md:h-10 rounded-md sm:rounded-lg bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center flex-shrink-0">
                    <span className="text-xs sm:text-sm md:text-base font-bold text-blue-600 dark:text-blue-400">1</span>
                  </div>
                  <p className="text-xs sm:text-sm md:text-base text-gray-700 dark:text-gray-300 w-full">
                    Break large tasks into smaller, manageable steps
                  </p>
                </div>
                <div className="flex items-start gap-2 sm:gap-3 w-full">
                  <div className="w-6 h-6 sm:w-8 sm:h-8 md:w-10 md:h-10 rounded-md sm:rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center flex-shrink-0">
                    <span className="text-xs sm:text-sm md:text-base font-bold text-purple-600 dark:text-purple-400">2</span>
                  </div>
                  <p className="text-xs sm:text-sm md:text-base text-gray-700 dark:text-gray-300 w-full">
                    Prioritize tasks using the Eisenhower Matrix
                  </p>
                </div>
                <div className="flex items-start gap-2 sm:gap-3 w-full">
                  <div className="w-6 h-6 sm:w-8 sm:h-8 md:w-10 md:h-10 rounded-md sm:rounded-lg bg-green-100 dark:bg-green-900/30 flex items-center justify-center flex-shrink-0">
                    <span className="text-xs sm:text-sm md:text-base font-bold text-green-600 dark:text-green-400">3</span>
                  </div>
                  <p className="text-xs sm:text-sm md:text-base text-gray-700 dark:text-gray-300 w-full">
                    Review and update your task list daily
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl sm:rounded-2xl border border-gray-200 dark:border-gray-700 p-4 sm:p-5 w-full">
              <h3 className="font-semibold text-gray-900 dark:text-white mb-3 sm:mb-4 text-sm sm:text-base md:text-lg w-full">Recent Activity</h3>
              <div className="space-y-3 sm:space-y-4 w-full">
                {tasks.slice(0, 5).map(task => (
                  <div key={task.id} className="flex items-center gap-2 sm:gap-3 w-full">
                    <div className={`w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full ${task.is_completed ? 'bg-green-500' : 'bg-amber-500'}`}></div>
                    <div className="flex-1 min-w-0 w-full">
                      <p className="text-xs sm:text-sm md:text-base font-medium text-gray-900 dark:text-white truncate w-full">
                        {task.title}
                      </p>
                      <p className="text-xs sm:text-sm text-gray-500 dark:text-gray-400 w-full">
                        {task.is_completed ? 'Completed' : 'In progress'}
                      </p>
                    </div>
                    <span className="text-xs sm:text-sm text-gray-500 dark:text-gray-400 whitespace-nowrap">
                      {new Date(task.updated_at || new Date()).toLocaleDateString('en-US', { 
                        month: 'short', 
                        day: 'numeric' 
                      })}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-gradient-to-br from-gray-900 to-gray-800 dark:from-gray-800 dark:to-gray-900 rounded-xl sm:rounded-2xl p-4 sm:p-5 text-white w-full">
              <h3 className="font-semibold mb-3 sm:mb-4 text-sm sm:text-base md:text-lg w-full">Quick Actions</h3>
              <div className="space-y-2 sm:space-y-3 w-full">
                <button
                  onClick={() => setIsCreateModalOpen(true)}
                  className="w-full flex items-center justify-between p-2.5 sm:p-3 md:p-3.5 rounded-lg sm:rounded-xl bg-white/10 hover:bg-white/20 transition-colors w-full"
                >
                  <div className="flex items-center gap-2 sm:gap-3 w-full">
                    <div className="w-6 h-6 sm:w-8 sm:h-8 md:w-10 md:h-10 rounded-md sm:rounded-lg bg-white/20 flex items-center justify-center">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 sm:h-4 sm:w-4 md:h-5 md:w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                      </svg>
                    </div>
                    <span className="text-xs sm:text-sm md:text-base font-medium">Add Quick Task</span>
                  </div>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 sm:h-4 sm:w-4 md:h-5 md:w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>
                <button
                  onClick={() => setFilter(null)}
                  className="w-full flex items-center justify-between p-2.5 sm:p-3 md:p-3.5 rounded-lg sm:rounded-xl bg-white/10 hover:bg-white/20 transition-colors w-full"
                >
                  <div className="flex items-center gap-2 sm:gap-3 w-full">
                    <div className="w-6 h-6 sm:w-8 sm:h-8 md:w-10 md:h-10 rounded-md sm:rounded-lg bg-white/20 flex items-center justify-center">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 sm:h-4 sm:w-4 md:h-5 md:w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                      </svg>
                    </div>
                    <span className="text-xs sm:text-sm md:text-base font-medium">View All Tasks</span>
                  </div>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 sm:h-4 sm:w-4 md:h-5 md:w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6 sm:mt-8 md:mt-12 py-4 sm:py-6 border-t border-gray-200 dark:border-gray-700 text-center text-xs sm:text-sm md:text-base text-gray-500 dark:text-gray-400 w-full px-2 sm:px-3 md:px-4">
          <p className="w-full">Showing {tasks.length} tasks • Last updated: {new Date().toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
          })} • {new Date().toLocaleDateString()}</p>
        </div>
      </div>

      <Modal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        title="Create New Task"
      >
        <TaskForm
          onSubmit={handleCreate}
          onCancel={() => setIsCreateModalOpen(false)}
          isSubmitting={isSubmitting}
        />
      </Modal>

      <Modal
        isOpen={!!editingTask}
        onClose={() => setEditingTask(null)}
        title="Edit Task"
      >
        {editingTask && (
          <TaskForm
            initialData={{
              title: editingTask.title,
              description: editingTask.description || "",
            }}
            onSubmit={handleEdit}
            onCancel={() => setEditingTask(null)}
            isSubmitting={isSubmitting}
            submitLabel="Save Changes"
          />
        )}
      </Modal>

      <DeleteConfirm
        isOpen={!!deletingTask}
        taskTitle={deletingTask?.title || ""}
        onConfirm={handleDelete}
        onCancel={() => setDeletingTask(null)}
        isDeleting={isSubmitting}
      />
    </div>
  );
}