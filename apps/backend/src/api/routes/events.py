"""
Events API endpoints.
Handles receiving and querying log/error events.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ...core.database import get_db
from ...models.event import Event
from ...schemas.event import EventCreate, EventResponse
from ...services.incident_service import IncidentService

router = APIRouter()


@router.post("/events", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    """
    Receive a new log/error event from an application.
    
    This endpoint:
    1. Stores the event in the database
    2. Checks if it should trigger a new incident
    3. Links to existing open incident if applicable
    
    **Request Body:**
    ```json
    {
        "service": "payment-service",
        "level": "ERROR",
        "message": "Database connection timeout"
    }
    ```
    
    **Response:** The created event with ID and timestamp
    """
    # Create event
    db_event = Event(
        service=event.service,
        level=event.level,
        message=event.message,
        timestamp=datetime.utcnow()
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    # Initialize incident service
    incident_service = IncidentService(db)
    
    # Only process ERROR events for incident detection
    if event.level == "ERROR":
        # Check if there's an open incident for this service
        open_incident = incident_service.get_open_incident_for_service(event.service)
        
        if open_incident:
            # Add to existing incident
            incident_service.add_event_to_incident(db_event, open_incident)
        else:
            # Check if we should create a new incident
            new_incident = incident_service.detect_and_group_incident(event.service)
            if new_incident:
                print(f"🚨 New incident created: ID={new_incident.id} for service={new_incident.service}")
    
    db.refresh(db_event)
    return db_event


@router.get("/events", response_model=List[EventResponse])
def list_events(
    skip: int = 0,
    limit: int = 100,
    service: str = None,
    level: str = None,
    db: Session = Depends(get_db)
):
    """
    List events with optional filtering.
    
    **Query Parameters:**
    - `skip`: Number of records to skip (pagination)
    - `limit`: Maximum number of records to return
    - `service`: Filter by service name
    - `level`: Filter by log level (ERROR, WARN, INFO)
    
    **Example:** `GET /api/v1/events?service=auth-api&level=ERROR&limit=50`
    """
    query = db.query(Event)
    
    if service:
        query = query.filter(Event.service == service)
    if level:
        query = query.filter(Event.level == level)
    
    events = query.order_by(Event.timestamp.desc()).offset(skip).limit(limit).all()
    return events


@router.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """
    Get a specific event by ID.
    
    **Path Parameter:**
    - `event_id`: The event ID
    
    **Response:** Event details with incident link if applicable
    """
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found"
        )
    return event
