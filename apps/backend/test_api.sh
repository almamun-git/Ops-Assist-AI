#!/bin/bash
# Quick test script for Ops-Assist AI backend

echo "🧪 Testing Ops-Assist AI Backend"
echo "================================="
echo ""

API_URL="http://localhost:8000"

# Test 1: Health Check
echo "1️⃣ Testing Health Endpoint..."
curl -s "$API_URL/health" | python3 -m json.tool
echo -e "\n"

# Test 2: Send some INFO events (should NOT create incident)
echo "2️⃣ Sending INFO events (no incident expected)..."
for i in {1..3}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"test-service\",\"level\":\"INFO\",\"message\":\"Normal operation #$i\"}" > /dev/null
  echo "  ✓ Sent INFO event #$i"
done
echo ""

# Test 3: Send ERROR events to trigger incident
echo "3️⃣ Sending 5 ERROR events (should trigger incident with AI analysis)..."
for i in {1..5}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"payment-service\",\"level\":\"ERROR\",\"message\":\"Database connection timeout - unable to acquire connection from pool #$i\"}" > /dev/null
  echo "  ✓ Sent ERROR event #$i"
  sleep 0.5
done
echo ""

# Wait for processing
sleep 2

# Test 4: Check incidents
echo "4️⃣ Checking Created Incidents..."
curl -s "$API_URL/api/v1/incidents" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'Total incidents: {len(data)}')
for incident in data:
    print(f'')
    print(f'🔴 Incident #{incident[\"id\"]}')
    print(f'   Service: {incident[\"service\"]}')
    print(f'   Status: {incident[\"status\"]}')
    print(f'   Events: {incident[\"event_count\"]}')
    if incident.get('category'):
        print(f'   🤖 AI Analysis:')
        print(f'      Category: {incident.get(\"category\", \"N/A\")}')
        print(f'      Severity: {incident.get(\"severity\", \"N/A\")}')
        print(f'      Summary: {incident.get(\"summary\", \"N/A\")[:80]}...')
"
echo ""

# Test 5: Get detailed incident info
echo "5️⃣ Getting Detailed Incident Info..."
INCIDENT_ID=$(curl -s "$API_URL/api/v1/incidents" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data[0]['id'] if data else '')")

if [ -n "$INCIDENT_ID" ]; then
  curl -s "$API_URL/api/v1/incidents/$INCIDENT_ID" | python3 -c "
import sys, json
incident = json.load(sys.stdin)
print(f'Incident Details:')
print(f'  ID: {incident[\"id\"]}')
print(f'  Service: {incident[\"service\"]}')
print(f'  Category: {incident.get(\"category\", \"N/A\")}')
print(f'  Severity: {incident.get(\"severity\", \"N/A\")}')
print(f'  Status: {incident[\"status\"]}')
print(f'  Summary: {incident.get(\"summary\", \"N/A\")}')
print(f'  Recommended Actions:')
for action in incident.get('recommended_actions', []):
    print(f'    - {action}')
print(f'  Total Events: {len(incident.get(\"events\", []))}')
"
fi

echo ""
echo "✅ Tests Complete!"
echo ""
echo "📖 Next Steps:"
echo "  - Visit http://localhost:8000/docs for interactive API documentation"
echo "  - Check incidents: curl http://localhost:8000/api/v1/incidents"
echo "  - View events: curl http://localhost:8000/api/v1/events"
