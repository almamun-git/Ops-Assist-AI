"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import get_settings
from .core.database import engine, Base
from .api.routes import events, incidents

settings = get_settings()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Ops-Assist AI",
    description="Intelligent Incident Management Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
# Note: Wildcards in origins don't work in FastAPI/Starlette
# We use allow_origin_regex for pattern matching instead
import re

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https://.*\.vercel\.app|http://localhost:3000|https://.*\.railway\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoints
@app.get("/")
def root():
    """Root endpoint - API status."""
    return {
        "message": "Ops-Assist AI - Intelligent Incident Management Platform",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "environment": settings.environment
    }


# Include API routes
app.include_router(events.router, prefix="/api/v1", tags=["Events"])
app.include_router(incidents.router, prefix="/api/v1", tags=["Incidents"])