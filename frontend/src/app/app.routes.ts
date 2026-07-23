/**
 * TaskFlow Frontend - App Routes
 * JIRA Story: TFLOW-6 - [FE] Setup Angular project with routing
 * 
 * Application route configuration with lazy loading.
 */

import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'tasks',
    pathMatch: 'full'
  },
  {
    path: 'tasks',
    loadComponent: () => 
      import('./components/task-list/task-list.component')
        .then(m => m.TaskListComponent),
    title: 'Tasks - TaskFlow'
  },
  {
    path: 'tasks/new',
    loadComponent: () => 
      import('./components/task-form/task-form.component')
        .then(m => m.TaskFormComponent),
    title: 'New Task - TaskFlow'
  },
  {
    path: 'tasks/:id/edit',
    loadComponent: () => 
      import('./components/task-form/task-form.component')
        .then(m => m.TaskFormComponent),
    title: 'Edit Task - TaskFlow'
  },
  {
    path: '**',
    redirectTo: 'tasks'
  }
];
