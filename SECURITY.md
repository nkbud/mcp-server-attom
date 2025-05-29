# Security Policy

## Supported Versions

We currently support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| Latest  | :white_check_mark: |
| < Latest| :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

1. **Do not** open a public issue for security vulnerabilities
2. Send an email to the project maintainer at: nicholasbudzban@gmail.com
3. Include as much detail as possible about the vulnerability
4. Allow reasonable time for the issue to be addressed before public disclosure

## Security Measures

This project implements the following security measures:

### Automated Security Scanning
- **CodeQL Analysis**: Automated code security scanning on every PR and weekly
- **Dependency Review**: All dependency changes are reviewed for known vulnerabilities
- **Dependabot**: Automated dependency updates with security patches

### Build Pipeline Security
- **Minimal Permissions**: CI/CD workflows follow principle of least privilege
- **Secure Actions**: Only use trusted, maintained GitHub Actions
- **Trusted Publishing**: PyPI publishing uses OIDC for secure, keyless publishing
- **Lockfile Verification**: Dependencies are pinned and verified via lockfiles

### Development Security
- **Code Quality**: Automated linting and formatting checks
- **Test Coverage**: Comprehensive test coverage requirements
- **Branch Protection**: Main branch is protected with required status checks

## Security Best Practices for Contributors

1. **Dependencies**: Always use the latest secure versions
2. **Secrets**: Never commit API keys, tokens, or sensitive data
3. **Code Review**: All changes require review before merging
4. **Testing**: Include security-focused tests when relevant

## Security Updates

Security updates will be released as soon as possible after discovery and verification of vulnerabilities. Updates will be communicated through:

- GitHub Security Advisories
- Release notes
- Project README updates

## Contact

For security-related questions or concerns, contact: nicholasbudzban@gmail.com