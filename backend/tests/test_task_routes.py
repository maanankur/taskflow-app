"""
TaskFlow Backend - Task Routes Tests

Tests the ROUTE layer's HTTP contract specifically (status codes, response
shape, pagination fields, validation edge cases) - a narrower lens than
backend/tests/test_tasks.py's broader end-to-end feature tests, so the two
files complement rather than duplicate each other.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db


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


client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """
    Create tables before each test and drop after. Claims the get_db
    override only while THIS file's tests are running (not as a bare
    module-level assignment) - app.dependency_overrides is a dict on the
    shared FastAPI app singleton, so a permanent assignment here would get
    silently overwritten by another test file's own override the moment
    both are collected in the same pytest run, pointing this file's
    requests at the wrong (or already-dropped) database.
    """
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.pop(get_db, None)


class TestCreateTaskRoute:
    def test_returns_201_and_full_task_shape(self):
        response = client.post("/api/tasks", json={"title": "Ship the release notes"})
        assert response.status_code == 201
        body = response.json()
        for field in ("id", "title", "description", "status", "priority", "due_date", "created_at", "updated_at"):
            assert field in body

    def test_rejects_title_over_255_chars(self):
        response = client.post("/api/tasks", json={"title": "x" * 256})
        assert response.status_code == 422

    def test_rejects_unknown_status_value(self):
        response = client.post("/api/tasks", json={"title": "Bad status", "status": "NOT_A_REAL_STATUS"})
        assert response.status_code == 422


class TestGetTasksRoute:
    def test_pagination_fields_present(self):
        response = client.get("/api/tasks")
        assert response.status_code == 200
        body = response.json()
        for field in ("items", "total", "page", "limit", "pages"):
            assert field in body

    def test_limit_is_respected(self):
        for i in range(3):
            client.post("/api/tasks", json={"title": f"Task {i}"})
        response = client.get("/api/tasks?limit=2")
        assert response.status_code == 200
        assert len(response.json()["items"]) == 2

    def test_limit_over_100_is_rejected(self):
        response = client.get("/api/tasks?limit=101")
        assert response.status_code == 422


class TestGetTaskRoute:
    def test_returns_404_with_task_id_in_detail(self):
        response = client.get("/api/tasks/9999")
        assert response.status_code == 404
        assert "9999" in response.json()["detail"]


class TestUpdateTaskRoute:
    def test_partial_update_leaves_other_fields_untouched(self):
        created = client.post("/api/tasks", json={"title": "Original", "priority": "HIGH"}).json()
        response = client.put(f"/api/tasks/{created['id']}", json={"status": "DONE"})
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "DONE"
        assert body["priority"] == "HIGH"  # untouched by the partial update
        assert body["title"] == "Original"


class TestDeleteTaskRoute:
    def test_delete_returns_204_with_empty_body(self):
        created = client.post("/api/tasks", json={"title": "To remove"}).json()
        response = client.delete(f"/api/tasks/{created['id']}")
        assert response.status_code == 204
        assert response.content == b""
