"""
Pydantic schemas for Incident API responses.
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .event import EventResponse


class IncidentResponse(BaseModel):
    """
    Schema for incident list responses.
    Used in GET /api/v1/incidents
    """
    id: int
    service: str
    category: Optional[str] = None
    severity: Optional[str] = None
    summary: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    event_count: int = 0  # Will be computed
    
    class Config:
        from_attributes = True


class IncidentDetail(BaseModel):
    """
    Schema for detailed incident response.
    Used in GET /api/v1/incidents/{id}
    Includes all related events.
    """
    id: int
    service: str
    category: Optional[str] = None
    severity: Optional[str] = None
    summary: Optional[str] = None
    recommended_actions: Optional[List[str]] = None
    status: str
    created_at: datetime
    updated_at: datetime
    events: List[EventResponse] = []
    
    class Config:
        from_attributes = True
