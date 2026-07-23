/**
 * TaskFlow Frontend - Task Service
 * JIRA Story: TFLOW-7 - [FE] Create Task service for API communication
 * 
 * HTTP service for Task CRUD operations.
 */

import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject, catchError, throwError, tap, finalize } from 'rxjs';

import { environment } from '../../environments/environment';
import { Task, TaskCreate, TaskUpdate, PaginatedResponse, TaskFilter } from '../models/task.model';

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  private http = inject(HttpClient);
  private apiUrl = `${environment.apiUrl}/tasks`;
  
  // Loading state observable
  private loadingSubject = new BehaviorSubject<boolean>(false);
  loading$ = this.loadingSubject.asObservable();

  /**
   * Fetch all tasks with optional filters
   */
  getTasks(filter?: TaskFilter): Observable<PaginatedResponse<Task>> {
    this.loadingSubject.next(true);
    
    let params = new HttpParams();
    if (filter) {
      if (filter.status) params = params.set('status', filter.status);
      if (filter.priority) params = params.set('priority', filter.priority);
      if (filter.search) params = params.set('search', filter.search);
      if (filter.page) params = params.set('page', filter.page.toString());
      if (filter.limit) params = params.set('limit', filter.limit.toString());
    }

    return this.http.get<PaginatedResponse<Task>>(this.apiUrl, { params }).pipe(
      finalize(() => this.loadingSubject.next(false)),
      catchError(this.handleError)
    );
  }

  /**
   * Fetch single task by ID
   */
  getTask(id: number): Observable<Task> {
    this.loadingSubject.next(true);
    
    return this.http.get<Task>(`${this.apiUrl}/${id}`).pipe(
      finalize(() => this.loadingSubject.next(false)),
      catchError(this.handleError)
    );
  }

  /**
   * Create new task
   */
  createTask(task: TaskCreate): Observable<Task> {
    this.loadingSubject.next(true);
    
    return this.http.post<Task>(this.apiUrl, task).pipe(
      finalize(() => this.loadingSubject.next(false)),
      catchError(this.handleError)
    );
  }

  /**
   * Update existing task
   */
  updateTask(id: number, task: TaskUpdate): Observable<Task> {
    this.loadingSubject.next(true);
    
    return this.http.put<Task>(`${this.apiUrl}/${id}`, task).pipe(
      finalize(() => this.loadingSubject.next(false)),
      catchError(this.handleError)
    );
  }

  /**
   * Delete task
   */
  deleteTask(id: number): Observable<void> {
    this.loadingSubject.next(true);
    
    return this.http.delete<void>(`${this.apiUrl}/${id}`).pipe(
      finalize(() => this.loadingSubject.next(false)),
      catchError(this.handleError)
    );
  }

  /**
   * Handle HTTP errors
   */
  private handleError(error: any): Observable<never> {
    console.error('TaskService error:', error);
    const message = error.error?.detail || error.message || 'An error occurred';
    return throwError(() => new Error(message));
  }
}
