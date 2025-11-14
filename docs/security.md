# Security Documentation

This document outlines the security measures implemented in the WallCod Portfolio & API project.

## Security Features

### 1. Authentication & Authorization

#### JWT-based Authentication

- **Access Tokens**: Short-lived tokens (30 minutes default)
- **Refresh Tokens**: Long-lived tokens (7 days default)
- **Token Rotation**: New tokens issued on refresh
- **Secure Storage**: Tokens stored in httpOnly cookies (recommended) or localStorage

#### Password Security

- **Hashing**: Bcrypt with automatic salt generation
- **Strength Requirements**:
  - Minimum 8 characters
  - At least one uppercase letter
  - At least one lowercase letter
  - At least one digit
  - At least one special character

```python
# Password validation example
def validate_password_strength(password: str) -> bool:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not any(c.isupper() for c in password):
        raise ValueError("Password must contain uppercase letter")
    if not any(c.islower() for c in password):
        raise ValueError("Password must contain lowercase letter")
    if not any(c.isdigit() for c in password):
        raise ValueError("Password must contain digit")
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        raise ValueError("Password must contain special character")
    return True
```

### 2. Input Validation & Sanitization

#### Backend Validation

- **Pydantic Schemas**: Type validation and coercion
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries
- **XSS Prevention**: Input sanitization and output encoding
- **CSRF Protection**: Token-based validation

```python
# Input sanitization example
def sanitize_input(input_string: str) -> str:
    # Remove null bytes
    sanitized = input_string.replace('\0', '')
    # Remove control characters
    sanitized = ''.join(char for char in sanitized
                       if ord(char) >= 32 or char in '\n\t')
    # Strip whitespace
    return sanitized.strip()
```

#### Frontend Validation

- **Zod Schemas**: Runtime type checking
- **React Hook Form**: Client-side validation
- **HTML Sanitization**: DOMPurify for user-generated content

### 3. API Security

#### Rate Limiting

```python
# Rate limiting configuration
RATE_LIMIT_PER_MINUTE = 60
RATE_LIMIT_PER_HOUR = 1000

@limiter.limit("60/minute")
async def protected_endpoint():
    pass
```

#### CORS Configuration

```python
# CORS settings
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://wallcod.com"
]
ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH"]
ALLOWED_HEADERS = ["*"]
```

#### Security Headers

```python
# Security headers
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
```

### 4. Database Security

#### Connection Security

- **SSL/TLS**: Encrypted connections to database
- **Connection Pooling**: Limited connection pool size
- **Prepared Statements**: Parameterized queries via SQLAlchemy

#### Access Control

```python
# Database user permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES
IN SCHEMA public TO wallcod;

# Revoke dangerous permissions
REVOKE CREATE ON SCHEMA public FROM wallcod;
```

#### Data Encryption

- **At Rest**: Database encryption (PostgreSQL TDE)
- **In Transit**: SSL/TLS connections
- **Sensitive Fields**: Additional encryption for PII

### 5. Container Security

#### Docker Best Practices

```dockerfile
# Use specific version tags
FROM python:3.11-slim

# Run as non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Scan for vulnerabilities
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*
```

#### Image Scanning

```yaml
# Trivy security scanning
- name: Run Trivy scanner
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'image'
    image-ref: 'wallcod-backend:latest'
    severity: 'CRITICAL,HIGH'
```

### 6. Secrets Management

#### Environment Variables

```bash
# Never commit secrets to git
echo ".env" >> .gitignore
echo "*.pem" >> .gitignore
echo "*.key" >> .gitignore
```

#### Secret Rotation

- Rotate secrets regularly (every 90 days)
- Use secret management tools (AWS Secrets Manager, HashiCorp Vault)
- Implement automated rotation policies

### 7. Logging & Monitoring

#### Security Logging

```python
# Log security events
logger.info(f"Login attempt for user: {username}")
logger.warning(f"Failed login attempt from IP: {ip_address}")
logger.error(f"Unauthorized access attempt to: {endpoint}")
```

#### Monitoring

- **Failed Login Attempts**: Track and alert on brute force attempts
- **API Rate Limiting**: Monitor for DDoS attempts
- **Error Rates**: Alert on unusual error patterns
- **Security Events**: Log all authentication events

### 8. Dependency Security

#### Automated Scanning

```yaml
# GitHub Actions - Security scanning
- name: Run safety check
  run: |
    pip install safety
    safety check --json

- name: Run Snyk
  uses: snyk/actions/node@master
  env:
    SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

#### Update Policy

- Review dependencies monthly
- Apply security patches immediately
- Use Dependabot for automated updates

### 9. Code Security

#### Static Analysis

```yaml
# Bandit for Python security issues
bandit -r app/ -ll

# ESLint for JavaScript security
eslint --ext .js,.ts,.tsx src/
```

#### Code Review

- All PRs require review
- Security-focused code review checklist
- Automated security checks in CI/CD

### 10. Network Security

#### HTTPS Only

```nginx
# Nginx SSL configuration
server {
    listen 443 ssl http2;
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    return 301 https://$server_name$request_uri;
}
```

#### Firewall Rules

```bash
# Allow only necessary ports
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 22/tcp
ufw enable
```

## Security Checklist

### Development

- [ ] Use HTTPS in all environments
- [ ] Validate and sanitize all inputs
- [ ] Use parameterized queries
- [ ] Implement rate limiting
- [ ] Set security headers
- [ ] Enable CORS properly
- [ ] Use strong password policies
- [ ] Implement JWT with refresh tokens
- [ ] Log security events
- [ ] Scan dependencies regularly

### Deployment

- [ ] Change default credentials
- [ ] Rotate secrets
- [ ] Enable database encryption
- [ ] Configure firewall rules
- [ ] Set up SSL/TLS
- [ ] Enable monitoring and alerts
- [ ] Implement backup strategy
- [ ] Use non-root users
- [ ] Disable debug mode
- [ ] Review security headers

### Ongoing

- [ ] Regular security audits
- [ ] Penetration testing
- [ ] Dependency updates
- [ ] Security training
- [ ] Incident response plan
- [ ] Regular backups
- [ ] Log review
- [ ] Access review

## Common Vulnerabilities & Mitigations

### SQL Injection

**Risk**: Attacker executes arbitrary SQL
**Mitigation**: Use ORM with parameterized queries

### Cross-Site Scripting (XSS)

**Risk**: Injection of malicious scripts
**Mitigation**: Input sanitization, output encoding, CSP headers

### Cross-Site Request Forgery (CSRF)

**Risk**: Unauthorized actions on behalf of user
**Mitigation**: CSRF tokens, SameSite cookies

### Authentication Bypass

**Risk**: Unauthorized access
**Mitigation**: Strong password policies, MFA, rate limiting

### Insecure Direct Object References

**Risk**: Unauthorized data access
**Mitigation**: Authorization checks, object-level permissions

### Security Misconfiguration

**Risk**: Default credentials, exposed admin panels
**Mitigation**: Security hardening, regular audits

### Sensitive Data Exposure

**Risk**: Leak of sensitive information
**Mitigation**: Encryption, proper access controls

## Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email security concerns to: [security@alphalabs.lat]
3. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work with you to resolve the issue.

## Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## Compliance

This project follows security best practices from:

- OWASP Application Security Verification Standard (ASVS)
- NIST Cybersecurity Framework
- CIS Controls
- GDPR privacy requirements
