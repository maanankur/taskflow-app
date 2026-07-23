/**
 * TaskFlow Frontend - Task Model
 * JIRA Story: TFLOW-7 - [FE] Create Task service for API communication
 * 
 * TypeScript interfaces for Task data.
 */

export type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'DONE';
export type TaskPriority = 'LOW' | 'MEDIUM' | 'HIGH';

/**
 * Task interface matching backend model
 */
export interface Task {
  id: number;
  title: string;
  description: string | null;
  status: TaskStatus;
  priority: TaskPriority;
  due_date: string | null;
  created_at: string;
  updated_at: string;
}

/**
 * Interface for creating a new task
 */
export interface TaskCreate {
  title: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  due_date?: string;
}

/**
 * Interface for updating a task
 */
export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: TaskStatus;
  priority?: TaskPriority;
  due_date?: string;
}

/**
 * Paginated response from API
 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

/**
 * Task filter options
 */
export interface TaskFilter {
  status?: TaskStatus;
  priority?: TaskPriority;
  search?: string;
  page?: number;
  limit?: number;
}
