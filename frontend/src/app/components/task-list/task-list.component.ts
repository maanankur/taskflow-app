/**
 * TaskFlow Frontend - Task List Component
 * JIRA Story: TFLOW-8 - [FE] Build Task List component
 * 
 * Displays list of tasks with filters and status indicators.
 */

import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';

import { TaskService } from '../../services/task.service';
import { Task, TaskStatus, TaskPriority, TaskFilter, PaginatedResponse } from '../../models/task.model';

@Component({
  selector: 'app-task-list',
  standalone: true,
  imports: [CommonModule, RouterLink, FormsModule],
  templateUrl: './task-list.component.html',
  styleUrl: './task-list.component.css'
})
export class TaskListComponent implements OnInit {
  private taskService = inject(TaskService);
  
  tasks: Task[] = [];
  loading$ = this.taskService.loading$;
  error: string | null = null;
  
  // Pagination
  currentPage = 1;
  totalPages = 1;
  totalItems = 0;
  
  // Filters
  filter: TaskFilter = {
    status: undefined,
    priority: undefined,
    search: ''
  };

  ngOnInit(): void {
    this.loadTasks();
  }

  /**
   * Load tasks from API with current filters
   */
  loadTasks(): void {
    this.error = null;
    const filter: TaskFilter = {
      ...this.filter,
      page: this.currentPage,
      limit: 10
    };
    
    // Remove empty values
    if (!filter.status) delete filter.status;
    if (!filter.priority) delete filter.priority;
    if (!filter.search) delete filter.search;
    
    this.taskService.getTasks(filter).subscribe({
      next: (response: PaginatedResponse<Task>) => {
        this.tasks = response.items;
        this.totalItems = response.total;
        this.totalPages = response.pages;
      },
      error: (err) => {
        this.error = err.message;
        this.tasks = [];
      }
    });
  }

  /**
   * Handle task row click - navigate to edit
   */
  onTaskClick(task: Task): void {
    // Navigation handled by routerLink in template
  }

  /**
   * Delete task with confirmation
   */
  onDeleteTask(task: Task, event: Event): void {
    event.stopPropagation();
    
    if (confirm(`Delete task "${task.title}"?`)) {
      this.taskService.deleteTask(task.id).subscribe({
        next: () => {
          this.loadTasks();
        },
        error: (err) => {
          this.error = err.message;
        }
      });
    }
  }

  /**
   * Apply filters and reload
   */
  applyFilter(): void {
    this.currentPage = 1;
    this.loadTasks();
  }

  /**
   * Clear all filters
   */
  clearFilters(): void {
    this.filter = {
      status: undefined,
      priority: undefined,
      search: ''
    };
    this.currentPage = 1;
    this.loadTasks();
  }

  /**
   * Go to page
   */
  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
      this.loadTasks();
    }
  }

  /**
   * Get status badge class
   */
  getStatusClass(status: TaskStatus): string {
    const classes: Record<TaskStatus, string> = {
      'TODO': 'badge-secondary',
      'IN_PROGRESS': 'badge-primary',
      'DONE': 'badge-success'
    };
    return classes[status] || 'badge-secondary';
  }

  /**
   * Get priority badge class
   */
  getPriorityClass(priority: TaskPriority): string {
    const classes: Record<TaskPriority, string> = {
      'LOW': 'badge-success',
      'MEDIUM': 'badge-warning',
      'HIGH': 'badge-danger'
    };
    return classes[priority] || 'badge-secondary';
  }

  /**
   * Format date for display
   */
  formatDate(dateString: string | null): string {
    if (!dateString) return '-';
    return new Date(dateString).toLocaleDateString();
  }
}
