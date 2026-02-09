// Auth Types
export interface User {
  userId: string;
  email: string;
}

export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface SignInCredentials {
  email: string;
  password: string;
}

export interface SignUpCredentials {
  firstName: string;
  lastName: string;
  email: string;
  password: string;
  confirmPassword: string;
}

// Task Types
export interface Task {
  id: string | number;
  title: string;
  description: string | null;
  is_completed: boolean;
  user_id: string;
  created_at: string;
  updated_at: string;
  due_date?: string | null;
  priority?: string;
  tags?: string[];
  recurrence_rule?: Record<string, any>;
  reminder_sent?: boolean;
}

export interface TaskCreateData {
  title: string;
  description?: string;
  is_completed?: boolean;
  due_date?: string;
  priority?: string;
  tags?: string[];
  recurrence_rule?: Record<string, any>;
}

export interface TaskUpdateData {
  title?: string;
  description?: string;
  is_completed?: boolean;
  due_date?: string;
  priority?: string;
  tags?: string[];
  recurrence_rule?: Record<string, any>;
  reminder_sent?: boolean;
}

export interface TaskListResponse {
  items: Task[];
  total: number;
  limit: number;
  offset: number;
}

export interface TaskQueryParams {
  is_completed?: boolean;
  limit?: number;
  offset?: number;
}

// Tasks State
export interface TasksState {
  items: Task[];
  total: number;
  isLoading: boolean;
  error: string | null;
  filter: {
    isCompleted: boolean | null;
  };
  pagination: {
    limit: number;
    offset: number;
  };
}

// API Error Types
export interface ErrorResponse {
  detail: string;
  error_code: string | null;
  timestamp: string;
}

// Form Types
export interface TaskFormData {
  title: string;
  description?: string;
  due_date?: string;
  priority?: string;
  tags?: string[];
  recurrence_rule?: {
    enabled: boolean;
    frequency: 'daily' | 'weekly' | 'monthly' | 'yearly';
    interval: number;
  };
}

// Toast Types
export type ToastType = 'success' | 'error' | 'info' | 'warning';

export interface Toast {
  id: string;
  message: string;
  type: ToastType;
  duration?: number;
}
