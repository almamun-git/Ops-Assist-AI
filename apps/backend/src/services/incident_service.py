"""
Incident detection and management service.
Automatically groups events into incidents based on time windows.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import Optional
from ..models.event import Event
from ..models.incident import Incident, IncidentStatus
from ..core.config import get_settings

settings = get_settings()


class IncidentService:
    """
    Service for detecting and managing incidents.
    
    Detection Logic:
    - If ≥5 ERROR events from same service within 5 minutes → Create incident
    - Group all those events under the new incident
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def detect_and_group_incident(self, service: str) -> Optional[Incident]:
        """
        Check if recent events should trigger a new incident.
        
        Args:
            service: The service name to check
            
        Returns:
            New incident if threshold met, None otherwise
        """
        # Calculate time window
        time_threshold = datetime.utcnow() - timedelta(
            seconds=settings.incident_time_window
        )
        
        # Find ERROR events from this service in time window that are NOT in an incident
        recent_errors = (
            self.db.query(Event)
            .filter(
                and_(
                    Event.service == service,
                    Event.level == "ERROR",
                    Event.timestamp >= time_threshold,
                    Event.incident_id.is_(None)  # Not already in an incident
                )
            )
            .all()
        )
        
        # Check if threshold met
        if len(recent_errors) >= settings.incident_threshold:
            # Create new incident
            incident = Incident(
                service=service,
                status=IncidentStatus.OPEN,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            self.db.add(incident)
            self.db.flush()  # Get the incident ID
            
            # Link all recent errors to this incident
            for event in recent_errors:
                event.incident_id = incident.id
            
            self.db.commit()
            self.db.refresh(incident)
            
            return incident
        
        return None
    
    def get_open_incident_for_service(self, service: str) -> Optional[Incident]:
        """
        Get the most recent OPEN incident for a service.
        Used to add new events to existing incidents.
        
        Args:
            service: The service name
            
        Returns:
            Most recent open incident or None
        """
        return (
            self.db.query(Incident)
            .filter(
                and_(
                    Incident.service == service,
                    Incident.status == IncidentStatus.OPEN
                )
            )
            .order_by(Incident.created_at.desc())
            .first()
        )
    
    def add_event_to_incident(self, event: Event, incident: Incident) -> None:
        """
        Add an event to an existing incident.
        
        Args:
            event: The event to add
            incident: The incident to add it to
        """
        event.incident_id = incident.id
        incident.updated_at = datetime.utcnow()
        self.db.commit()
    
    def get_incident_with_events(self, incident_id: int) -> Optional[Incident]:
        """
        Get an incident with all its events loaded.
        
        Args:
            incident_id: The incident ID
            
        Returns:
            Incident with events or None
        """
        return (
            self.db.query(Incident)
            .filter(Incident.id == incident_id)
            .first()
        )
    
    def list_incidents(
        self, 
        skip: int = 0, 
        limit: int = 100,
        status: Optional[str] = None
    ) -> list[Incident]:
        """
        List incidents with pagination.
        
        Args:
            skip: Number of records to skip
            limit: Maximum records to return
            status: Filter by status (optional)
            
        Returns:
            List of incidents
        """
        query = self.db.query(Incident)
        
        if status:
            query = query.filter(Incident.status == status)
        
        return (
            query
            .order_by(Incident.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
