"""
Incidents API endpoints.
Handles querying and managing incidents.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ...core.database import get_db
from ...models.incident import Incident
from ...schemas.incident import IncidentResponse, IncidentDetail
from ...services.incident_service import IncidentService

router = APIRouter()


@router.get("/incidents", response_model=List[IncidentResponse])
def list_incidents(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List all incidents with pagination and optional status filtering.
    
    **Query Parameters:**
    - `skip`: Number of records to skip (default: 0)
    - `limit`: Maximum records to return (default: 100)
    - `status_filter`: Filter by status (open, investigating, resolved, closed)
    
    **Example:** `GET /api/v1/incidents?status_filter=open&limit=20`
    
    **Response:** List of incidents with event counts
    """
    incident_service = IncidentService(db)
    incidents = incident_service.list_incidents(
        skip=skip,
        limit=limit,
        status=status_filter
    )
    
    # Add event count to each incident
    result = []
    for incident in incidents:
        incident_dict = {
            "id": incident.id,
            "service": incident.service,
            "category": incident.category,
            "severity": incident.severity,
            "summary": incident.summary,
            "status": incident.status.value,
            "created_at": incident.created_at,
            "updated_at": incident.updated_at,
            "event_count": len(incident.events) if incident.events else 0
        }
        result.append(IncidentResponse(**incident_dict))
    
    return result


@router.get("/incidents/{incident_id}", response_model=IncidentDetail)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    """
    Get detailed information about a specific incident.
    
    **Path Parameter:**
    - `incident_id`: The incident ID
    
    **Response:** Complete incident details including all related events
    
    **Example Response:**
    ```json
    {
        "id": 1,
        "service": "payment-service",
        "category": "database_issue",
        "severity": "P1",
        "summary": "Database connection timeouts causing payment failures",
        "recommended_actions": ["restart_db_service", "scale_db"],
        "status": "open",
        "events": [...]
    }
    ```
    """
    incident_service = IncidentService(db)
    incident = incident_service.get_incident_with_events(incident_id)
    
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident with id {incident_id} not found"
        )
    
    return incident


@router.patch("/incidents/{incident_id}/status")
def update_incident_status(
    incident_id: int,
    new_status: str,
    db: Session = Depends(get_db)
):
    """
    Update the status of an incident.
    
    **Path Parameter:**
    - `incident_id`: The incident ID
    
    **Query Parameter:**
    - `new_status`: New status (open, investigating, resolved, closed)
    
    **Example:** `PATCH /api/v1/incidents/1/status?new_status=investigating`
    """
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    
    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Incident with id {incident_id} not found"
        )
    
    # Validate status
    valid_statuses = ["open", "investigating", "resolved", "closed"]
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    # Update status
    from ...models.incident import IncidentStatus
    incident.status = IncidentStatus(new_status)
    db.commit()
    
    return {
        "message": "Incident status updated successfully",
        "incident_id": incident_id,
        "new_status": new_status
    }