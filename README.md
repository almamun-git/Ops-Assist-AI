# 🚀 Intelligent Incident Workflow Assistant

[![CI](https://github.com/almamun-git/Intelligent-Incident-Workflow-Assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/almamun-git/Intelligent-Incident-Workflow-Assistant/actions/workflows/ci.yml)
[![CodeQL](https://github.com/almamun-git/Intelligent-Incident-Workflow-Assistant/actions/workflows/codeql.yml/badge.svg)](https://github.com/almamun-git/Intelligent-Incident-Workflow-Assistant/actions/workflows/codeql.yml)
[![codecov](https://codecov.io/gh/almamun-git/Intelligent-Incident-Workflow-Assistant/branch/main/graph/badge.svg)](https://codecov.io/gh/almamun-git/Intelligent-Incident-Workflow-Assistant)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AI-powered platform for real-time incident detection, classification, and analytics.

---

## 🧠 Overview

Intelligent Incident Workflow Assistant helps engineering and DevOps teams detect and triage production issues faster by:

- Streaming and storing application events/logs
- Automatically grouping spikes of errors into incidents
- Using AI to classify category and severity and suggest actions
- Providing a modern dashboard to monitor status and trends

Under the hood, it’s a full-stack app built with FastAPI, PostgreSQL, and a Next.js dashboard. If an OpenAI API key isn’t configured, the AI layer gracefully falls back to a deterministic mock for local testing.

---

## ✨ Core Features

- Real-time event ingestion and querying
- Automatic incident detection (threshold + time window)
- AI-powered classification (category, severity, summary, actions)

---

## Repo layout (high level)

```
apps/
  backend/   # FastAPI backend (src/, tests, scripts)
  frontend/  # Next.js dashboard (TypeScript, Tailwind)
packages/shared/ # shared types
RUNNING.md
DEPLOYMENT.md
README.md
```

---

## Tech stack

- Frontend: Next.js 14, React, TypeScript, TailwindCSS
- Backend: FastAPI, SQLAlchemy (models), Uvicorn
- DB: PostgreSQL (local) / Supabase (hosted)
- AI: OpenAI API with deterministic mock fallback for local/dev
- Deploy: Render / Vercel / Railway (deployment docs included)

---

## Quickstart (local)

1) Clone

```bash
git clone https://github.com/almamun-git/Intelligent-Incident-Workflow-Assistant.git
cd Intelligent-Incident-Workflow-Assistant
```

2) Backend

```bash
cd apps/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# create .env (example)
cat > .env <<'EOF'
DATABASE_URL=postgresql://postgres@localhost:5432/ops_assist_ai
OPENAI_API_KEY= # optional; leave empty to use mock
INCIDENT_THRESHOLD=5
INCIDENT_TIME_WINDOW=300
EOF

uvicorn src.main:app --reload --port 8000
```

3) Frontend

```bash
cd ../frontend
npm install
npm run dev
```

- Backend: http://localhost:8000 (interactive API docs at `/docs`)
- Frontend: http://localhost:3000

---

## API — quick reference

Deployed base: https://ops-assist-ai.onrender.com/

Local base (when running locally): http://localhost:8000/

Selected endpoints

- Health
  - GET /health
  - Response: { "status": "healthy", "environment": "development" }

- Events
  - POST /api/v1/events
    - Body example: { "service": "payment-service", "level": "ERROR", "message": "Database connection timeout" }
  - GET /api/v1/events?service=service-name&level=ERROR&limit=50

- Incidents
  - GET /api/v1/incidents?status_filter=open&limit=20
  - GET /api/v1/incidents/{id}
  - PATCH /api/v1/incidents/{id}/status — body: { "status": "investigating" }
  - POST /api/v1/incidents/{id}/analyze — re-run AI analysis for an incident

Detection rule (default): INCIDENT_THRESHOLD=5 and INCIDENT_TIME_WINDOW=300s → opens an incident when threshold reached for a service (configurable via env vars).

Example (list incidents — deployed):

```bash
curl -sS "https://ops-assist-ai.onrender.com/api/v1/incidents" -H "Accept: application/json"
```

Example (create event — local):

```bash
curl -X POST http://localhost:8000/api/v1/events \
  -H "Content-Type: application/json" \
  -d '{"service":"payment-service","level":"ERROR","message":"Database connection timeout"}'
```

For the complete, interactive API spec visit the deployed docs: https://ops-assist-ai.onrender.com/docs

---

## Notes for contributors / developers

- AI layer: If `OPENAI_API_KEY` is missing the code falls back to a deterministic/mock analyzer to allow offline testing.
- Frontend reads the API base from a helper (`apps/frontend/src/lib/api.ts`) — update that or set the correct env when developing locally.
- Tests and quick scripts: `apps/backend/test_api.sh`, `apps/backend/create_incidents.sh`, `apps/backend/test_demo.py` help exercise flows.

---

## Contributing

PRs welcome. For docs updates, keep the README's API links in sync with the deployed `/docs` OpenAPI spec. See `DEPLOYMENT.md` and `RUNNING.md` for environment and deployment information.

---

## Author

Abdullah Al Mamun Apu — https://github.com/almamun-git — https://mamunapu.tech

---

## License

MIT
