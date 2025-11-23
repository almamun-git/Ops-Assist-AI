# Security Policy

## Reporting a Vulnerability

We take the security of Intelligent Incident Workflow Assistant seriously. If you discover a security vulnerability, please follow these steps:

### Reporting Process

1. **Do NOT** open a public GitHub issue for security vulnerabilities
2. Email security reports to: **almamun.apu@gmail.com**
3. Include the following information in your report:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact and severity assessment
   - Any suggested fixes or mitigations (if available)

### What to Expect

- **Initial Response**: We will acknowledge receipt of your vulnerability report within 48 hours
- **Investigation**: Our team will investigate and validate the reported vulnerability
- **Updates**: We will keep you informed about the progress of addressing the issue
- **Resolution**: Once fixed, we will notify you and may publicly disclose the vulnerability (with credit to you, if desired)

### Response Timeline

- **Critical vulnerabilities**: Addressed within 7 days
- **High severity**: Addressed within 14 days
- **Medium severity**: Addressed within 30 days
- **Low severity**: Addressed within 60 days

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Security Best Practices

When deploying this application:

1. **Environment Variables**: Never commit sensitive credentials to version control
2. **API Keys**: Secure your OpenAI API keys and database credentials
3. **Database**: Use strong passwords and restrict database access
4. **HTTPS**: Always use HTTPS in production environments
5. **Dependencies**: Keep dependencies up to date using Dependabot
6. **Access Control**: Implement appropriate authentication and authorization

## Known Security Considerations

- The application uses OpenAI API for incident analysis. Ensure your API key is properly secured
- PostgreSQL connections should use SSL in production
- CORS is configured for specific origins; review and adjust for your deployment

## Security Features

- CodeQL security scanning on every PR and push to main
- Automated dependency updates via Dependabot
- Coverage requirements to ensure code quality
- Regular security audits through GitHub Advanced Security

Thank you for helping keep Intelligent Incident Workflow Assistant secure!
