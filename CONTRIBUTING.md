# Contributing to Intelligent Incident Workflow Assistant

Thank you for your interest in contributing to this project! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL (for local development)
- Git

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd apps/backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with required environment variables:
   ```bash
   DATABASE_URL=postgresql://postgres@localhost:5432/ops_assist_ai
   OPENAI_API_KEY=  # optional; leave empty to use mock
   INCIDENT_THRESHOLD=5
   INCIDENT_TIME_WINDOW=300
   ```

5. Run the backend:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd apps/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at http://localhost:3000 and the backend at http://localhost:8000.

## Running Tests

### Backend Tests

```bash
cd apps/backend
pytest --cov=src --cov-report=term
```

### Frontend Tests

```bash
cd apps/frontend
npm test
```

## Code Quality

### Linting

- Backend: Follow PEP 8 style guidelines
- Frontend: Run `npm run lint` to check for issues

### Coverage Requirements

- Backend: Minimum 75% coverage (configured in `.coveragerc`)
- Frontend: 
  - Branches: 65%
  - Functions: 70%
  - Lines: 75%
  - Statements: 75%

## Branching Strategy

- `main` - Production-ready code
- `feature/*` - New features
- `fix/*` - Bug fixes
- `chore/*` - Maintenance tasks
- `docs/*` - Documentation updates

## Pull Request Process

1. Fork the repository and create a new branch from `main`
2. Make your changes following the coding standards
3. Write or update tests as necessary
4. Ensure all tests pass and coverage requirements are met
5. Update documentation if you're changing functionality
6. Submit a pull request with a clear description of the changes

### PR Guidelines

- Use conventional commit messages (feat:, fix:, docs:, chore:, etc.)
- Keep PRs focused on a single concern
- Include tests for new functionality
- Update the CHANGELOG.md if appropriate
- Link related issues in the PR description

## Architecture Overview

### Backend (FastAPI)

- `src/main.py` - Application entry point
- `src/api/routes/` - API endpoints
- `src/models/` - SQLAlchemy database models
- `src/schemas/` - Pydantic schemas for validation
- `src/services/` - Business logic
- `src/core/` - Configuration and database setup

### Frontend (Next.js)

- `src/app/` - Next.js 14 App Router pages
- `src/components/` - React components
- `src/lib/` - Utility functions and helpers

### Key Features

- Real-time event ingestion and storage
- Automatic incident detection based on error thresholds
- AI-powered incident classification and analysis
- Modern dashboard for monitoring and triage

## Security

Please review our [SECURITY.md](SECURITY.md) for information on reporting security vulnerabilities.

## Questions?

Feel free to open an issue for questions or clarifications about contributing.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
