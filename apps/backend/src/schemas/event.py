"""
Pydantic schemas for Event API requests and responses.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class EventCreate(BaseModel):
    """
    Schema for creating a new event.
    Used when receiving logs/errors from applications.
    
    Example:
        {
            "service": "auth-api",
            "level": "ERROR",
            "message": "Database connection timeout"
        }
    """
    service: str = Field(..., min_length=1, max_length=100, description="Service name")
    level: str = Field(..., description="Log level (ERROR, WARN, INFO)")
    message: str = Field(..., min_length=1, description="Error/log message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "service": "payment-service",
                "level": "ERROR",
                "message": "Failed to process payment: Connection timeout to payment gateway"
            }
        }


class EventResponse(BaseModel):
    """
    Schema for event responses.
    Returned when querying events.
    """
    id: int
    service: str
    level: str
    message: str
    timestamp: datetime
    incident_id: Optional[int] = None
    
    class Config:
        from_attributes = True  # Allows creating from SQLAlchemy models
