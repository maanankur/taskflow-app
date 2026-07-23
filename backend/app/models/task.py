"""
TaskFlow Backend - Task Model
JIRA Story: TFLOW-3 - [BE] Create Task model and database schema

SQLAlchemy model for Task entity with status and priority enums.
"""

from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum
from app.database import Base


class TaskStatus(str, PyEnum):
    """Enum for task status values."""
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class TaskPriority(str, PyEnum):
    """Enum for task priority values."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Task(Base):
    """
    Task database model.
    
    Attributes:
        id: Primary key
        title: Task title (required)
        description: Task description (optional)
        status: Current status (TODO, IN_PROGRESS, DONE)
        priority: Priority level (LOW, MEDIUM, HIGH)
        due_date: Optional due date
        created_at: Timestamp when created
        updated_at: Timestamp when last updated
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status={self.status})>"
