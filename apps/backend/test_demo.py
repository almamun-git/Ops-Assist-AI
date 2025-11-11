#!/usr/bin/env python3
"""
Test script to demonstrate the Ops-Assist AI incident management system.
Sends events to the API and triggers incident creation.
"""
import requests
import time
import json

API_BASE_URL = "http://localhost:8000/api/v1"

def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}\n")

def send_event(service, level, message):
    """Send an event to the API."""
    url = f"{API_BASE_URL}/events"
    payload = {
        "service": service,
        "level": level,
        "message": message
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 201:
        event = response.json()
        print(f"✅ Event created: ID={event['id']}, Service={event['service']}, Level={event['level']}")
        if event.get('incident_id'):
            print(f"   ⚠️  Linked to Incident ID: {event['incident_id']}")
        return event
    else:
        print(f"❌ Failed to create event: {response.status_code}")
        print(f"   {response.text}")
        return None

def get_incidents():
    """Get all incidents."""
    url = f"{API_BASE_URL}/incidents"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

def get_incident_detail(incident_id):
    """Get detailed incident information."""
    url = f"{API_BASE_URL}/incidents/{incident_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def main():
    print_section("🚀 Ops-Assist AI - Incident Management Demo")
    
    # Test 1: Send normal log events (should NOT create incident)
    print_section("Test 1: Send INFO events (no incident expected)")
    for i in range(3):
        send_event("payment-service", "INFO", f"Payment processed successfully #{i+1}")
        time.sleep(0.5)
    
    # Test 2: Send 3 ERROR events (below threshold, no incident)
    print_section("Test 2: Send 3 ERROR events (below threshold)")
    for i in range(3):
        send_event("payment-service", "ERROR", f"Database connection timeout #{i+1}")
        time.sleep(0.5)
    
    # Test 3: Send 2 more ERROR events (5 total, should trigger incident)
    print_section("Test 3: Send 2 more ERROR events (INCIDENT TRIGGER)")
    for i in range(2):
        send_event("payment-service", "ERROR", f"Database connection timeout #{i+4}")
        time.sleep(0.5)
    
    # Wait a bit for processing
    time.sleep(1)
    
    # Check incidents
    print_section("📊 Incidents Created")
    incidents = get_incidents()
    print(f"Total incidents: {len(incidents)}")
    
    for incident in incidents:
        print(f"\n🔴 Incident #{incident['id']}")
        print(f"   Service: {incident['service']}")
        print(f"   Status: {incident['status']}")
        print(f"   Events: {incident['event_count']}")
        print(f"   Created: {incident['created_at']}")
        
        # Get detailed info
        detail = get_incident_detail(incident['id'])
        if detail:
            # Show AI analysis if available
            if detail.get('category'):
                print(f"\n   🤖 AI Analysis:")
                print(f"      Category: {detail['category']}")
                print(f"      Severity: {detail['severity']}")
                print(f"      Summary: {detail['summary']}")
                if detail.get('recommended_actions'):
                    print(f"      Actions: {', '.join(detail['recommended_actions'][:3])}")
            
            print(f"\n   📝 Events in this incident:")
            for event in detail['events'][:3]:  # Show first 3
                print(f"      - [{event['timestamp']}] {event['message'][:50]}...")
            if len(detail['events']) > 3:
                print(f"      ... and {len(detail['events']) - 3} more events")
    
    # Test 4: Send ERROR from different service
    print_section("Test 4: Different service (should create separate incident)")
    for i in range(5):
        send_event("auth-api", "ERROR", f"JWT validation failed #{i+1}")
        time.sleep(0.3)
    
    # Final incidents check
    print_section("📊 Final Incidents Summary")
    incidents = get_incidents()
    print(f"Total incidents: {len(incidents)}\n")
    
    for incident in incidents:
        print(f"Incident #{incident['id']}: {incident['service']} - {incident['event_count']} events")
    
    print_section("✅ Demo Complete!")
    print("Visit http://localhost:8000/docs to explore the API interactively")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API at http://localhost:8000")
        print("Make sure the FastAPI server is running:")
        print("   cd apps/backend && venv/bin/uvicorn src.main:app --reload")
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
