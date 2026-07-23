"""
TaskFlow Backend - Task Schemas
JIRA Story: TFLOW-3 - [BE] Create Task model and database schema

Pydantic schemas for Task API request/response validation.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.models.task import TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    """Schema for creating a new task."""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: TaskStatus = Field(default=TaskStatus.TODO, description="Task status")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Task priority")
    due_date: Optional[datetime] = Field(None, description="Due date")


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: Optional[TaskStatus] = Field(None, description="Task status")
    priority: Optional[TaskPriority] = Field(None, description="Task priority")
    due_date: Optional[datetime] = Field(None, description="Due date")


class TaskResponse(BaseModel):
    """Schema for task API response."""
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode for SQLAlchemy models
