"""
TaskFlow Backend - Task Routes
JIRA Story: TFLOW-4 - [BE] Implement Task CRUD API endpoints
JIRA Story: TFLOW-5 - [BE] Add task filtering and search

REST API endpoints for Task CRUD operations.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.task import TaskStatus, TaskPriority
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse
from app.services import task_service

router = APIRouter()


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    """
    Create a new task.
    
    - **title**: Task title (required, 1-255 chars)
    - **description**: Task description (optional)
    - **status**: TODO, IN_PROGRESS, or DONE (default: TODO)
    - **priority**: LOW, MEDIUM, or HIGH (default: MEDIUM)
    - **due_date**: Optional due date
    """
    return task_service.create_task(db, task_data)


@router.get("/tasks", response_model=dict)
def get_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filter by status"),
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority"),
    search: Optional[str] = Query(None, description="Search in title/description"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    Get all tasks with optional filtering and pagination.
    
    JIRA Story: TFLOW-5 - Add filtering capability
    
    - **status**: Filter by TODO, IN_PROGRESS, or DONE
    - **priority**: Filter by LOW, MEDIUM, or HIGH
    - **search**: Search term for title and description
    - **page**: Page number (default: 1)
    - **limit**: Items per page (default: 10, max: 100)
    """
    result = task_service.get_filtered_tasks(
        db, status=status, priority=priority, search=search, page=page, limit=limit
    )
    
    # Convert Task objects to response format
    return {
        "items": [TaskResponse.model_validate(task) for task in result["items"]],
        "total": result["total"],
        "page": result["page"],
        "limit": result["limit"],
        "pages": result["pages"]
    }


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    Get a task by ID.
    
    - **task_id**: Task ID to retrieve
    
    Raises:
        404: Task not found
    """
    task = task_service.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    """
    Update a task by ID.
    
    - **task_id**: Task ID to update
    - Only provided fields will be updated (partial update)
    
    Raises:
        404: Task not found
    """
    task = task_service.update_task(db, task_id, task_data)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Delete a task by ID.
    
    - **task_id**: Task ID to delete
    
    Raises:
        404: Task not found
    """
    deleted = task_service.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return None
