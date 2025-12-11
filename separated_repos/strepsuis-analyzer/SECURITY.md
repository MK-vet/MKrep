# Security Policy

## Supported Versions

Currently supported versions of StrepSuisAnalyzer:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please follow these steps:

### How to Report

**DO NOT** open a public issue for security vulnerabilities.

Instead, please report security issues by:

1. Creating a private security advisory on GitHub
2. Emailing the maintainers directly (see repository contact information)

### What to Include

Please include the following information:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if available)
- Your contact information

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity
  - Critical: Within 7 days
  - High: Within 14 days
  - Medium: Within 30 days
  - Low: Next scheduled release

## Security Best Practices

When using StrepSuisAnalyzer:

1. **Keep Dependencies Updated**: Regularly update dependencies to receive security patches
2. **Validate Input Data**: Always validate and sanitize input data
3. **Use HTTPS**: When deploying, use HTTPS for encrypted communication
4. **Access Control**: Implement proper authentication and authorization
5. **Data Privacy**: Ensure compliance with data protection regulations
6. **File Upload Security**: Validate file types and sizes
7. **Docker Security**: Use official base images and keep them updated

## Security Considerations

### Data Handling

- StrepSuisAnalyzer processes genomic and phenotypic data locally
- No data is transmitted to external servers by default
- Ensure compliance with institutional data policies

### File Upload

- The application validates file types and formats
- Implement file size limits in production deployments
- Scan uploaded files for malware in production environments

### Dependencies

- All dependencies are vetted for known vulnerabilities
- Regular dependency updates are performed
- Use `pip-audit` or similar tools to check for vulnerabilities

### Docker Deployment

- Use non-root user in Docker containers
- Limit container resources
- Keep base images updated
- Follow Docker security best practices

## Disclosure Policy

When a security issue is reported:

1. We will investigate and confirm the vulnerability
2. We will develop and test a fix
3. We will release the fix in a new version
4. We will publicly disclose the vulnerability after the fix is released
5. We will credit the reporter (unless they prefer to remain anonymous)

## Security Updates

Security updates will be released as:

- Patch versions for backward-compatible security fixes
- Documentation will be updated to reflect security changes
- Release notes will clearly indicate security-related changes

## Contact

For security concerns, please contact the maintainers through GitHub or the repository's designated security channels.

---

Last updated: 2025-01-15
