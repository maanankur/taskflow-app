"""
TaskFlow Backend - Task Service
JIRA Story: TFLOW-4 - [BE] Implement Task CRUD API endpoints
JIRA Story: TFLOW-5 - [BE] Add task filtering and search

Business logic layer for Task operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.task_schema import TaskCreate, TaskUpdate


def create_task(db: Session, task_data: TaskCreate) -> Task:
    """
    Create a new task in the database.
    
    Args:
        db: Database session
        task_data: Task creation data
        
    Returns:
        Task: Created task instance
    """
    db_task = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        priority=task_data.priority,
        due_date=task_data.due_date
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_all_tasks(db: Session) -> List[Task]:
    """
    Retrieve all tasks from the database.
    
    Args:
        db: Database session
        
    Returns:
        List[Task]: List of all tasks
    """
    return db.query(Task).order_by(Task.created_at.desc()).all()


def get_task_by_id(db: Session, task_id: int) -> Optional[Task]:
    """
    Retrieve a task by its ID.
    
    Args:
        db: Database session
        task_id: Task ID to find
        
    Returns:
        Optional[Task]: Task if found, None otherwise
    """
    return db.query(Task).filter(Task.id == task_id).first()


def update_task(db: Session, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
    """
    Update an existing task.
    
    Args:
        db: Database session
        task_id: Task ID to update
        task_data: Update data (partial update supported)
        
    Returns:
        Optional[Task]: Updated task if found, None otherwise
    """
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return None
    
    # Update only provided fields
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    """
    Delete a task from the database.
    
    Args:
        db: Database session
        task_id: Task ID to delete
        
    Returns:
        bool: True if deleted, False if not found
    """
    db_task = get_task_by_id(db, task_id)
    if not db_task:
        return False
    
    db.delete(db_task)
    db.commit()
    return True


def get_filtered_tasks(
    db: Session,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 10
) -> dict:
    """
    Filter and search tasks with pagination.
    
    JIRA Story: TFLOW-5 - [BE] Add task filtering and search
    
    Args:
        db: Database session
        status: Filter by status (optional)
        priority: Filter by priority (optional)
        search: Search term for title/description (optional)
        page: Page number (1-indexed)
        limit: Items per page
        
    Returns:
        dict: Paginated results with total count
    """
    query = db.query(Task)
    
    # Apply filters
    if status:
        query = query.filter(Task.status == status)
    
    if priority:
        query = query.filter(Task.priority == priority)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                Task.title.ilike(search_term),
                Task.description.ilike(search_term)
            )
        )
    
    # Get total count before pagination
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * limit
    tasks = query.order_by(Task.created_at.desc()).offset(offset).limit(limit).all()
    
    return {
        "items": tasks,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    }

