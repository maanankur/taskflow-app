"""
TaskFlow Backend - FastAPI Application
JIRA Story: TFLOW-2 - [BE] Setup FastAPI project structure

This is the main entry point for the TaskFlow API.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routes import task_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler - creates database tables on startup."""
    # Create all database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup (if needed) goes here


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    app = FastAPI(
        title="TaskFlow API",
        description="Task Management API for Context Orchestrator POC",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # Configure CORS for frontend communication
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4200"],  # Angular dev server
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register routes
    app.include_router(task_routes.router, prefix="/api", tags=["tasks"])
    
    return app


# Create application instance
app = create_app()


@app.get("/api/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status
    """
    return {"status": "ok", "service": "taskflow-api", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
