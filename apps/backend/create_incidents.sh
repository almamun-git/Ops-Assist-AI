#!/bin/bash
# Script to create various test incidents

API_URL="${1:-http://localhost:8000}"

echo "🚀 Creating Test Incidents..."
echo "API URL: $API_URL"
echo ""

# Incident 1: Database Issues (P1 - Critical)
echo "📊 Creating Database Incident (Critical)..."
for i in {1..6}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"user-service\",\"level\":\"ERROR\",\"message\":\"PostgreSQL connection pool exhausted - max connections reached\"}" > /dev/null
  sleep 0.3
done
echo "  ✅ Created database incident"
echo ""

# Incident 2: API Gateway Timeouts (P2 - High)
echo "🌐 Creating API Gateway Incident (High Priority)..."
for i in {1..5}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"api-gateway\",\"level\":\"ERROR\",\"message\":\"Gateway timeout: upstream service not responding within 30s\"}" > /dev/null
  sleep 0.3
done
echo "  ✅ Created API gateway incident"
echo ""

# Incident 3: Memory Issues (P1 - Critical)
echo "💾 Creating Memory Incident (Critical)..."
for i in {1..7}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"analytics-worker\",\"level\":\"ERROR\",\"message\":\"Out of memory error: heap size exceeded, GC overhead limit\"}" > /dev/null
  sleep 0.3
done
echo "  ✅ Created memory incident"
echo ""

# Incident 4: Authentication Failures (P2)
echo "🔐 Creating Auth Incident (High Priority)..."
for i in {1..5}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"auth-service\",\"level\":\"ERROR\",\"message\":\"JWT token validation failed: signature verification error\"}" > /dev/null
  sleep 0.3
done
echo "  ✅ Created authentication incident"
echo ""

# Incident 5: Rate Limiting (P3 - Medium)
echo "⏱️  Creating Rate Limit Incident (Medium Priority)..."
for i in {1..5}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"public-api\",\"level\":\"WARNING\",\"message\":\"Rate limit exceeded: 1000 requests/min threshold breached\"}" > /dev/null
  sleep 0.3
done
echo "  ✅ Created rate limit incident"
echo ""

# Incident 6: Disk Space (P1 - Critical)
echo "💿 Creating Disk Space Incident (Critical)..."
for i in {1..6}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"storage-service\",\"level\":\"ERROR\",\"message\":\"Disk space critical: only 2% remaining on /var/log partition\"}" > /dev/null
  sleep 0.3
done
echo "  ✅ Created disk space incident"
echo ""

# Wait for AI processing
echo "⏳ Waiting for AI analysis..."
sleep 3

# Display results
echo ""
echo "📋 Fetching Created Incidents..."
curl -s "$API_URL/api/v1/incidents" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f'\n✨ Total Incidents: {len(data)}\n')
    for incident in data:
        severity_emoji = {'P1': '🔴', 'P2': '🟡', 'P3': '🟢'}.get(incident.get('severity', ''), '⚪')
        status_emoji = {'open': '🆕', 'investigating': '🔍', 'resolved': '✅', 'closed': '📦'}.get(incident.get('status', ''), '❓')
        print(f'{severity_emoji} {status_emoji} Incident #{incident[\"id\"]}')
        print(f'   Service: {incident[\"service\"]}')
        print(f'   Category: {incident.get(\"category\", \"N/A\")}')
        print(f'   Severity: {incident.get(\"severity\", \"N/A\")}')
        print(f'   Status: {incident[\"status\"]}')
        print(f'   Events: {incident[\"event_count\"]}')
        summary = incident.get('summary', '')
        if summary:
            print(f'   Summary: {summary[:80]}...' if len(summary) > 80 else f'   Summary: {summary}')
        print()
except Exception as e:
    print(f'Error: {e}')
"

echo ""
echo "✅ All incidents created!"
echo ""
echo "🎯 Next steps:"
echo "  - View dashboard: http://localhost:3000"
echo "  - API docs: $API_URL/docs"
echo "  - Update incident status from the UI"
