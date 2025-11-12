# How to Create Incidents in Ops-Assist AI

## Overview
Incidents are automatically created when 5+ error events occur within 5 minutes from the same service.

---

## Method 1: Run the Test Script (Easiest)

### Create multiple diverse incidents:
```bash
cd apps/backend
./create_incidents.sh
```

This creates 6 different incidents:
- 🔴 Database connection issues (Critical)
- 🟡 API Gateway timeouts (High)
- 🔴 Memory/OOM errors (Critical)
- 🟡 Authentication failures (High)
- 🟢 Rate limiting (Medium)
- 🔴 Disk space critical (Critical)

### For production (Render):
```bash
./create_incidents.sh https://ops-assist-ai.onrender.com
```

---

## Method 2: Using cURL (Manual)

### Send error events to create an incident:

```bash
# Define your API URL
API_URL="http://localhost:8000"

# Send 5+ error events from the same service within 5 minutes
for i in {1..5}; do
  curl -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{
      \"service\": \"my-service\",
      \"level\": \"ERROR\",
      \"message\": \"Something went wrong: error #$i\"
    }"
  sleep 1
done
```

### Common incident scenarios:

#### Database Incident:
```bash
curl -X POST "http://localhost:8000/api/v1/events" \
  -H "Content-Type: application/json" \
  -d '{
    "service": "order-service",
    "level": "ERROR",
    "message": "Database connection timeout: failed to connect to PostgreSQL"
  }'
```

#### Memory/OOM Incident:
```bash
curl -X POST "http://localhost:8000/api/v1/events" \
  -H "Content-Type: application/json" \
  -d '{
    "service": "worker-service",
    "level": "ERROR",
    "message": "Out of memory: Java heap space exceeded"
  }'
```

#### Network Incident:
```bash
curl -X POST "http://localhost:8000/api/v1/events" \
  -H "Content-Type: application/json" \
  -d '{
    "service": "api-gateway",
    "level": "ERROR",
    "message": "Connection refused: upstream service unavailable"
  }'
```

#### Authentication Incident:
```bash
curl -X POST "http://localhost:8000/api/v1/events" \
  -H "Content-Type: application/json" \
  -d '{
    "service": "auth-service",
    "level": "ERROR",
    "message": "JWT token expired: authentication failed"
  }'
```

---

## Method 3: Using Python

### Quick Python script:
```python
import requests
import time

API_URL = "http://localhost:8000"

# Send multiple error events
for i in range(5):
    response = requests.post(
        f"{API_URL}/api/v1/events",
        json={
            "service": "python-service",
            "level": "ERROR",
            "message": f"Critical error occurred: event #{i+1}"
        }
    )
    print(f"Sent event {i+1}: {response.status_code}")
    time.sleep(0.5)

# Check incidents
incidents = requests.get(f"{API_URL}/api/v1/incidents").json()
print(f"\nTotal incidents: {len(incidents)}")
for incident in incidents:
    print(f"  - {incident['service']}: {incident['status']} ({incident['event_count']} events)")
```

---

## Method 4: Interactive API Docs

1. Go to http://localhost:8000/docs
2. Find **POST /api/v1/events**
3. Click **"Try it out"**
4. Enter JSON:
   ```json
   {
     "service": "test-service",
     "level": "ERROR",
     "message": "Test error message"
   }
   ```
5. Click **Execute**
6. Repeat 5+ times to create an incident

---

## Understanding the Incident Creation Logic

### When does an incident get created?
- **Threshold**: 5+ events
- **Time window**: Within 5 minutes
- **Same service**: All events must be from the same service
- **Error levels**: ERROR, CRITICAL, FATAL

### What events DON'T create incidents?
- INFO, DEBUG, WARNING levels (< 5 events)
- Events from different services
- Events spread over > 5 minutes

### AI Analysis
Once an incident is created, AI analyzes it and adds:
- **Category**: database_issue, network_issue, performance_issue, etc.
- **Severity**: P1 (Critical), P2 (High), P3 (Medium)
- **Summary**: Natural language description
- **Recommended Actions**: Steps to resolve

---

## Checking Your Incidents

### Via cURL:
```bash
# List all incidents
curl http://localhost:8000/api/v1/incidents | python3 -m json.tool

# Get specific incident
curl http://localhost:8000/api/v1/incidents/1 | python3 -m json.tool
```

### Via Browser:
- Dashboard: http://localhost:3000
- API Docs: http://localhost:8000/docs

### Via Database:
```bash
cd apps/backend
source venv/bin/activate
python3 -c "
from src.core.database import SessionLocal
from src.models.incident import Incident

db = SessionLocal()
incidents = db.query(Incident).all()
for i in incidents:
    print(f'{i.id}: {i.service} - {i.status} ({i.event_count} events)')
"
```

---

## Updating Incident Status

### Start investigation:
```bash
curl -X PATCH "http://localhost:8000/api/v1/incidents/1/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "investigating"}'
```

### Mark as resolved:
```bash
curl -X PATCH "http://localhost:8000/api/v1/incidents/1/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved"}'
```

### Close incident:
```bash
curl -X PATCH "http://localhost:8000/api/v1/incidents/1/status" \
  -H "Content-Type: application/json" \
  -d '{"status": "closed"}'
```

---

## Tips

1. **Batch create incidents**: Use the `create_incidents.sh` script for testing
2. **Real-world simulation**: Add delays between events to simulate real errors
3. **Different services**: Create incidents for different microservices to test filtering
4. **Status workflow**: Test the full workflow: open → investigating → resolved → closed
5. **AI analysis**: Check how AI categorizes different error messages
