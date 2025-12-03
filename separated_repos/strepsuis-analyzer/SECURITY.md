# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 2025.8.x| :white_check_mark: |
| < 2025.8| :x:                |

## Reporting a Vulnerability

The StrepSuis Analyzer team takes security bugs seriously. We appreciate your efforts to responsibly disclose your findings.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via one of the following methods:

1. **Email**: Send details to [security contact to be added]
2. **GitHub Security Advisories**: Use the "Security" tab in the repository

### What to Include

When reporting a vulnerability, please include:

- Type of issue (e.g., buffer overflow, SQL injection, cross-site scripting, etc.)
- Full paths of source file(s) related to the manifestation of the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution Target**: Within 90 days

## Security Best Practices

### For Users

1. **Keep Updated**: Always use the latest version
2. **Input Validation**: Validate all input data files
3. **File Permissions**: Ensure proper file permissions on data directories
4. **Docker Security**: Run Docker containers as non-root user (default in our images)
5. **Network Security**: Don't expose analysis servers to public networks

### For Developers

1. **No Eval/Exec**: Never use `eval()` or `exec()` with user input
2. **Path Validation**: Validate and sanitize all file paths
3. **Dependency Updates**: Keep dependencies up to date
4. **Code Review**: All code changes require review
5. **Static Analysis**: Use security scanning tools (Bandit, CodeQL)

## Known Security Considerations

### Data Privacy

- **User Data**: Analyzer processes genomic data which may be sensitive
- **Recommendation**: Use appropriate data handling procedures for sensitive datasets
- **No Data Collection**: This software does not collect or transmit user data

### File Handling

- **Input Validation**: All CSV files are validated before processing
- **Path Traversal**: Path traversal attacks are prevented through path validation
- **Temporary Files**: Temporary files are created securely and cleaned up

### Dependencies

We regularly monitor and update dependencies to address security vulnerabilities:

- Dependencies are pinned in `requirements.txt`
- Security updates are applied promptly
- Vulnerability scanning with `pip-audit` and Dependabot

### Docker Security

Our Docker images follow security best practices:

- Based on official Python slim images
- Non-root user by default
- Minimal attack surface (only necessary packages)
- Regular base image updates
- No secrets in images

## Security Updates

Security patches are released as soon as possible after a vulnerability is confirmed:

1. **Critical**: Within 24 hours
2. **High**: Within 7 days
3. **Medium**: Within 30 days
4. **Low**: Next regular release

## Vulnerability Disclosure Policy

- We follow coordinated vulnerability disclosure
- We will acknowledge receipt of your report
- We will provide a timeline for fixes
- We will credit you for the discovery (if desired)

## Security Tools

We use the following tools to maintain security:

- **Bandit**: Python security linter
- **CodeQL**: Semantic code analysis
- **Dependabot**: Automated dependency updates
- **pip-audit**: Python package vulnerability scanner
- **Pre-commit hooks**: Automated security checks

## Security Hall of Fame

We thank the following researchers for responsibly disclosing security issues:

(None yet - this is the initial release)

## Contact

For sensitive security matters, contact:
- [Security contact to be added]

For general questions:
- Open an issue on GitHub (for non-security issues)
- Refer to CONTRIBUTING.md for contribution guidelines

## Additional Resources

- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security.html)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)

---

**Last Updated**: 2025-08-11
