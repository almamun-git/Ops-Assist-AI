# Contributing to Intelligent Incident Workflow Assistant

## Vision
Reduce MTTR by automating incident detection, classification, and remediation hints with a clean, observable architecture.

## Ground Rules
- Conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`
- Add tests for new logic (FastAPI endpoints, utilities, React components)
- Keep PRs focused (< ~400 lines net change)
- Ensure lint + tests pass locally before opening a PR

## Backend Setup
```bash
cd apps/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## Frontend Setup
```bash
cd apps/frontend
npm install
npm run dev
```

## Tests
- Backend: `pytest`
- Frontend: `npm test`

## Branching
- Feature: `feat/<short-description>`
- Fix: `fix/<issue-number-or-short>`
- Chore: `chore/<scope>`
- Security: `sec/<scope>`

## Pull Requests
1. Reference issues (`Closes #XX`)
2. Describe the change (why + what)
3. Include perf/behavior before vs after when relevant
4. Update docs if API or behavior changed

## Architecture
- FastAPI backend (`apps/backend/src`): routers → services → persistence
- PostgreSQL via SQLAlchemy; threshold + window algorithm for incident detection
- AI analyzer falls back to deterministic mock when no key
- Next.js frontend queries API base defined in `apps/frontend/src/lib/api.ts`

## Security
See `SECURITY.md` for reporting guidelines.

## Releases
Initial manual tagging. Semantic release workflow planned.

## Getting Help
Open an issue with environment, steps, expected vs actual, and logs/traceback.

Thanks for contributing!
