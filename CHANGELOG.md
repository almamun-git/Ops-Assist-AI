# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - TBD

### Added

- CI/CD workflows for automated testing and code quality
  - GitHub Actions CI workflow for backend (Python/pytest) and frontend (Node/Jest) with Codecov integration
  - CodeQL analysis workflow for security scanning (Python and JavaScript)
  - Dependabot configuration for automated dependency updates
- Testing infrastructure
  - Backend: pytest configuration with coverage requirements (75% minimum)
  - Frontend: Jest configuration with coverage thresholds
  - Initial health endpoint test for backend
  - Minimal dummy test for frontend to validate test infrastructure
- Documentation
  - CONTRIBUTING.md with development setup and contribution guidelines
  - SECURITY.md with security vulnerability reporting process
  - CODEOWNERS file for code review assignments
  - Quality badges in README (CI, CodeQL, Coverage, License)
- Quality gates and standards
  - Branch coverage enabled for backend tests
  - Coverage thresholds enforced in CI
  - Code ownership and review requirements

### Changed

- README.md updated with badges and corrected repository clone URL
- README.md cleaned up duplicate heading section

### Planned

- Enhanced test coverage across backend and frontend
- Integration tests for API endpoints
- End-to-end tests for critical user workflows
- Performance benchmarking and monitoring
- Additional security scanning tools integration

[0.1.0]: https://github.com/almamun-git/Intelligent-Incident-Workflow-Assistant/releases/tag/v0.1.0
