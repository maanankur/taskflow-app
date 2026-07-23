/**
 * TaskFlow Frontend - Task Form Component
 * JIRA Story: TFLOW-9 - [FE] Build Task Form component for create/edit
 * 
 * Form for creating and editing tasks.
 */

import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, ActivatedRoute, RouterLink } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';

import { TaskService } from '../../services/task.service';
import { Task, TaskCreate, TaskUpdate, TaskStatus, TaskPriority } from '../../models/task.model';

@Component({
  selector: 'app-task-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './task-form.component.html',
  styleUrl: './task-form.component.css'
})
export class TaskFormComponent implements OnInit {
  private fb = inject(FormBuilder);
  private taskService = inject(TaskService);
  private router = inject(Router);
  private route = inject(ActivatedRoute);
  
  taskForm!: FormGroup;
  isEditMode = false;
  taskId: number | null = null;
  loading$ = this.taskService.loading$;
  error: string | null = null;
  successMessage: string | null = null;
  
  // Dropdown options
  statusOptions: TaskStatus[] = ['TODO', 'IN_PROGRESS', 'DONE'];
  priorityOptions: TaskPriority[] = ['LOW', 'MEDIUM', 'HIGH'];

  ngOnInit(): void {
    this.initForm();
    
    // Check if editing existing task
    const idParam = this.route.snapshot.paramMap.get('id');
    if (idParam) {
      this.taskId = parseInt(idParam, 10);
      this.isEditMode = true;
      this.loadTask();
    }
  }

  /**
   * Initialize reactive form with validators
   */
  private initForm(): void {
    this.taskForm = this.fb.group({
      title: ['', [Validators.required, Validators.minLength(3), Validators.maxLength(255)]],
      description: [''],
      status: ['TODO'],
      priority: ['MEDIUM'],
      due_date: ['']
    });
  }

  /**
   * Load existing task for edit mode
   */
  private loadTask(): void {
    if (!this.taskId) return;
    
    this.taskService.getTask(this.taskId).subscribe({
      next: (task: Task) => {
        // Format date for input
        const dueDate = task.due_date 
          ? new Date(task.due_date).toISOString().split('T')[0]
          : '';
        
        this.taskForm.patchValue({
          title: task.title,
          description: task.description || '',
          status: task.status,
          priority: task.priority,
          due_date: dueDate
        });
      },
      error: (err) => {
        this.error = err.message;
      }
    });
  }

  /**
   * Handle form submission
   */
  onSubmit(): void {
    if (this.taskForm.invalid) {
      this.taskForm.markAllAsTouched();
      return;
    }
    
    this.error = null;
    this.successMessage = null;
    
    const formValue = this.taskForm.value;
    
    // Convert date string to ISO format if provided
    if (formValue.due_date) {
      formValue.due_date = new Date(formValue.due_date).toISOString();
    } else {
      delete formValue.due_date;
    }
    
    if (this.isEditMode && this.taskId) {
      // Update existing task
      const updateData: TaskUpdate = formValue;
      
      this.taskService.updateTask(this.taskId, updateData).subscribe({
        next: () => {
          this.successMessage = 'Task updated successfully!';
          setTimeout(() => this.router.navigate(['/tasks']), 1000);
        },
        error: (err) => {
          this.error = err.message;
        }
      });
    } else {
      // Create new task
      const createData: TaskCreate = formValue;
      
      this.taskService.createTask(createData).subscribe({
        next: () => {
          this.successMessage = 'Task created successfully!';
          setTimeout(() => this.router.navigate(['/tasks']), 1000);
        },
        error: (err) => {
          this.error = err.message;
        }
      });
    }
  }

  /**
   * Cancel and return to list
   */
  onCancel(): void {
    this.router.navigate(['/tasks']);
  }

  /**
   * Check if form field has error
   */
  hasError(fieldName: string, errorType: string): boolean {
    const field = this.taskForm.get(fieldName);
    return field ? field.hasError(errorType) && field.touched : false;
  }
}
