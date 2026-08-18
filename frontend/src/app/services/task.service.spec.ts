/**
 * TaskFlow Frontend - Task Service Tests
 * Verifies TaskService issues the right HTTP request (method, URL, params,
 * body) for each CRUD operation, tracks loading$ correctly, and surfaces
 * backend errors instead of swallowing them.
 */
import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import { TaskService } from './task.service';
import { environment } from '../../environments/environment';
import { Task, TaskCreate } from '../models/task.model';

describe('TaskService', () => {
  let service: TaskService;
  let httpMock: HttpTestingController;
  const apiUrl = `${environment.apiUrl}/tasks`;

  const sampleTask: Task = {
    id: 1,
    title: 'Buy groceries',
    description: null,
    status: 'TODO',
    priority: 'MEDIUM',
    due_date: null,
    created_at: '2026-01-01T00:00:00Z',
    updated_at: '2026-01-01T00:00:00Z',
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [TaskService],
    });
    service = TestBed.inject(TaskService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('getTasks() issues a GET to the base tasks URL with filter params', () => {
    service.getTasks({ status: 'TODO', page: 1, limit: 10 }).subscribe((res) => {
      expect(res.items.length).toBe(1);
      expect(res.total).toBe(1);
    });

    const req = httpMock.expectOne(
      (r) => r.method === 'GET' && r.url === apiUrl && r.params.get('status') === 'TODO'
    );
    req.flush({ items: [sampleTask], total: 1, page: 1, limit: 10, pages: 1 });
  });

  it('getTask(id) issues a GET to /tasks/:id', () => {
    service.getTask(1).subscribe((task) => expect(task).toEqual(sampleTask));

    const req = httpMock.expectOne(`${apiUrl}/1`);
    expect(req.request.method).toBe('GET');
    req.flush(sampleTask);
  });

  it('createTask() posts the payload to the base tasks URL', () => {
    const payload: TaskCreate = { title: 'Buy groceries' };
    service.createTask(payload).subscribe((task) => expect(task.title).toBe('Buy groceries'));

    const req = httpMock.expectOne(apiUrl);
    expect(req.request.method).toBe('POST');
    expect(req.request.body).toEqual(payload);
    req.flush(sampleTask);
  });

  it('updateTask(id, patch) puts to /tasks/:id', () => {
    service.updateTask(1, { status: 'DONE' }).subscribe((task) => expect(task).toEqual(sampleTask));

    const req = httpMock.expectOne(`${apiUrl}/1`);
    expect(req.request.method).toBe('PUT');
    expect(req.request.body).toEqual({ status: 'DONE' });
    req.flush(sampleTask);
  });

  it('deleteTask(id) issues a DELETE to /tasks/:id', () => {
    service.deleteTask(1).subscribe();

    const req = httpMock.expectOne(`${apiUrl}/1`);
    expect(req.request.method).toBe('DELETE');
    req.flush(null);
  });

  it('toggles loading$ true then false around a request', (done) => {
    const seen: boolean[] = [];
    service.loading$.subscribe((v) => seen.push(v));

    service.getTasks().subscribe(() => {
      expect(seen).toEqual([false, true, false]);
      done();
    });

    httpMock.expectOne(apiUrl).flush({ items: [], total: 0, page: 1, limit: 10, pages: 0 });
  });

  it('surfaces a backend error via handleError() instead of swallowing it', (done) => {
    service.getTask(999).subscribe({
      next: () => fail('expected an error, got a successful response'),
      error: (err) => {
        expect(err).toBeTruthy();
        done();
      },
    });

    httpMock
      .expectOne(`${apiUrl}/999`)
      .flush({ detail: 'Task with id 999 not found' }, { status: 404, statusText: 'Not Found' });
  });
});
