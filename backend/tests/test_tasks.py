"""
TaskFlow Backend - Task Tests
Tests for Task API endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite://"  # In-memory database

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test and drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestHealthCheck:
    def test_health_check(self):
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestCreateTask:
    def test_create_task_success(self):
        response = client.post(
            "/api/tasks",
            json={"title": "Test Task", "description": "Test Description"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test Task"
        assert data["status"] == "TODO"
        assert data["priority"] == "MEDIUM"

    def test_create_task_minimal(self):
        response = client.post("/api/tasks", json={"title": "Minimal Task"})
        assert response.status_code == 201
        assert response.json()["title"] == "Minimal Task"

    def test_create_task_empty_title(self):
        response = client.post("/api/tasks", json={"title": ""})
        assert response.status_code == 422


class TestGetTasks:
    def test_get_tasks_empty(self):
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert response.json()["items"] == []
        assert response.json()["total"] == 0

    def test_get_tasks_with_data(self):
        # Create tasks
        client.post("/api/tasks", json={"title": "Task 1"})
        client.post("/api/tasks", json={"title": "Task 2"})
        
        response = client.get("/api/tasks")
        assert response.status_code == 200
        assert response.json()["total"] == 2


class TestGetTaskById:
    def test_get_task_success(self):
        # Create task
        create_response = client.post("/api/tasks", json={"title": "Test Task"})
        task_id = create_response.json()["id"]
        
        response = client.get(f"/api/tasks/{task_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Test Task"

    def test_get_task_not_found(self):
        response = client.get("/api/tasks/999")
        assert response.status_code == 404


class TestUpdateTask:
    def test_update_task_success(self):
        # Create task
        create_response = client.post("/api/tasks", json={"title": "Original"})
        task_id = create_response.json()["id"]
        
        response = client.put(
            f"/api/tasks/{task_id}",
            json={"title": "Updated", "status": "IN_PROGRESS"}
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Updated"
        assert response.json()["status"] == "IN_PROGRESS"

    def test_update_task_not_found(self):
        response = client.put("/api/tasks/999", json={"title": "Updated"})
        assert response.status_code == 404


class TestDeleteTask:
    def test_delete_task_success(self):
        # Create task
        create_response = client.post("/api/tasks", json={"title": "To Delete"})
        task_id = create_response.json()["id"]
        
        response = client.delete(f"/api/tasks/{task_id}")
        assert response.status_code == 204
        
        # Verify deleted
        get_response = client.get(f"/api/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_delete_task_not_found(self):
        response = client.delete("/api/tasks/999")
        assert response.status_code == 404


class TestFilterTasks:
    def test_filter_by_status(self):
        client.post("/api/tasks", json={"title": "Task 1", "status": "TODO"})
        client.post("/api/tasks", json={"title": "Task 2", "status": "DONE"})
        
        response = client.get("/api/tasks?status=TODO")
        assert response.status_code == 200
        assert response.json()["total"] == 1
        assert response.json()["items"][0]["status"] == "TODO"

    def test_filter_by_priority(self):
        client.post("/api/tasks", json={"title": "Task 1", "priority": "HIGH"})
        client.post("/api/tasks", json={"title": "Task 2", "priority": "LOW"})
        
        response = client.get("/api/tasks?priority=HIGH")
        assert response.status_code == 200
        assert response.json()["total"] == 1

    def test_search_tasks(self):
        client.post("/api/tasks", json={"title": "Buy groceries"})
        client.post("/api/tasks", json={"title": "Call mom"})
        
        response = client.get("/api/tasks?search=groceries")
        assert response.status_code == 200
        assert response.json()["total"] == 1
