#!/bin/bash
# Enhanced script with MORE incident scenarios

API_URL="${1:-http://localhost:8000}"

echo "🎨 Creating MORE Test Incidents..."
echo "API URL: $API_URL"
echo ""

# Incident 7: Redis Cache Failures
echo "🔴 Creating Redis Cache Incident..."
for i in {1..5}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"cache-service\",\"level\":\"ERROR\",\"message\":\"Redis connection lost: ECONNREFUSED - Cannot connect to Redis server\"}" > /dev/null
  sleep 0.3
done
echo "  ✅ Created Redis incident"
echo ""

# Incident 8: Kubernetes Pod Crashes
echo "☸️  Creating Kubernetes Incident..."
for i in {1..6}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"k8s-controller\",\"level\":\"ERROR\",\"message\":\"Pod crashed: CrashLoopBackOff - container exits with code 137\"}" > /dev/null
  sleep 0.3
done
echo "  ✅ Created Kubernetes incident"
echo ""

# Incident 9: Payment Gateway Failures
echo "💳 Creating Payment Gateway Incident..."
for i in {1..5}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"payment-gateway\",\"level\":\"ERROR\",\"message\":\"Stripe API error: card_declined - insufficient funds\"}" > /dev/null
  sleep 0.3
done
echo "  ✅ Created payment incident"
echo ""

# Incident 10: Email Service Down
echo "📧 Creating Email Service Incident..."
for i in {1..5}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"email-service\",\"level\":\"ERROR\",\"message\":\"SMTP connection failed: 554 relay access denied\"}" > /dev/null
  sleep 0.3
done
echo "  ✅ Created email incident"
echo ""

# Incident 11: Message Queue Backlog
echo "📮 Creating Queue Backlog Incident..."
for i in {1..6}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"rabbitmq\",\"level\":\"ERROR\",\"message\":\"Queue depth critical: 50000+ messages pending, consumers too slow\"}" > /dev/null
  sleep 0.3
done
echo "  ✅ Created queue incident"
echo ""

# Incident 12: SSL Certificate Expiry
echo "🔒 Creating SSL Certificate Incident..."
for i in {1..5}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"nginx\",\"level\":\"ERROR\",\"message\":\"SSL certificate expired: certificate is not valid after 2025-11-10\"}" > /dev/null
  sleep 0.3
done
echo "  ✅ Created SSL incident"
echo ""

# Incident 13: S3 Storage Failures
echo "☁️  Creating S3 Storage Incident..."
for i in {1..5}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"upload-service\",\"level\":\"ERROR\",\"message\":\"AWS S3 error: AccessDenied - insufficient permissions to write object\"}" > /dev/null
  sleep 0.3
done
echo "  ✅ Created S3 incident"
echo ""

# Incident 14: Load Balancer Health Check Failures
echo "⚖️  Creating Load Balancer Incident..."
for i in {1..6}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"load-balancer\",\"level\":\"ERROR\",\"message\":\"Health check failed: 3/5 backend servers not responding\"}" > /dev/null
  sleep 0.3
done
echo "  ✅ Created load balancer incident"
echo ""

# Incident 15: Elasticsearch Cluster Red
echo "🔍 Creating Elasticsearch Incident..."
for i in {1..5}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"search-service\",\"level\":\"ERROR\",\"message\":\"Elasticsearch cluster status RED: unassigned shards detected\"}" > /dev/null
  sleep 0.3
done
echo "  ✅ Created Elasticsearch incident"
echo ""

# Incident 16: Container Registry Pull Failures
echo "🐳 Creating Docker Registry Incident..."
for i in {1..5}; do
  curl -s -X POST "$API_URL/api/v1/events" \
    -H "Content-Type: application/json" \
    -d "{\"service\":\"docker-registry\",\"level\":\"ERROR\",\"message\":\"Image pull failed: manifest unknown - tag not found in registry\"}" > /dev/null
  sleep 0.3
done
echo "  ✅ Created Docker incident"
echo ""

echo "⏳ Waiting for AI analysis..."
sleep 3

echo ""
echo "✅ 10 more incidents created!"
echo ""
echo "📊 Total incidents in system now:"
curl -s "$API_URL/api/v1/incidents" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'  {len(data)} incidents')" 2>/dev/null || echo "  (Backend processing...)"
echo ""
