"""
Security examples and utilities for educational purposes.

This module demonstrates various security practices and common vulnerabilities.
Use these examples to understand security concepts and implement them correctly.
"""

import re
import hashlib
import secrets
import hmac
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import ipaddress


class SecurityExamples:
    """Collection of security examples and best practices."""

    # ============================================================================
    # INPUT VALIDATION & SANITIZATION
    # ============================================================================

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email address format.

        Args:
            email: Email address to validate

        Returns:
            bool: True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_username(username: str) -> bool:
        """
        Validate username format.

        Rules:
        - 3-50 characters
        - Only alphanumeric, underscore, hyphen
        - Cannot start with number

        Args:
            username: Username to validate

        Returns:
            bool: True if valid, False otherwise
        """
        if not 3 <= len(username) <= 50:
            return False

        pattern = r'^[a-zA-Z][a-zA-Z0-9_-]*$'
        return bool(re.match(pattern, username))

    @staticmethod
    def sanitize_html(html: str) -> str:
        """
        Sanitize HTML to prevent XSS attacks.

        This is a basic example. Use a library like bleach for production.

        Args:
            html: HTML string to sanitize

        Returns:
            str: Sanitized HTML
        """
        # Remove script tags
        html = re.sub(r'<script.*?>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)

        # Remove event handlers
        html = re.sub(r'\s*on\w+\s*=\s*["\'].*?["\']', '', html, flags=re.IGNORECASE)

        # Remove javascript: protocol
        html = re.sub(r'javascript:', '', html, flags=re.IGNORECASE)

        return html

    @staticmethod
    def validate_file_upload(filename: str, allowed_extensions: set) -> bool:
        """
        Validate file upload.

        Args:
            filename: Name of uploaded file
            allowed_extensions: Set of allowed file extensions

        Returns:
            bool: True if valid, False otherwise
        """
        # Check for path traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return False

        # Check extension
        extension = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        return extension in allowed_extensions

    # ============================================================================
    # CRYPTOGRAPHY
    # ============================================================================

    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """
        Generate a cryptographically secure random token.

        Args:
            length: Length of token in bytes

        Returns:
            str: URL-safe token
        """
        return secrets.token_urlsafe(length)

    @staticmethod
    def hash_data(data: str, salt: Optional[str] = None) -> tuple[str, str]:
        """
        Hash data with salt using SHA-256.

        Args:
            data: Data to hash
            salt: Optional salt (generated if not provided)

        Returns:
            tuple: (hash, salt)
        """
        if salt is None:
            salt = secrets.token_hex(16)

        hash_obj = hashlib.sha256()
        hash_obj.update(salt.encode() + data.encode())

        return hash_obj.hexdigest(), salt

    @staticmethod
    def verify_hash(data: str, hash_value: str, salt: str) -> bool:
        """
        Verify hashed data.

        Args:
            data: Original data
            hash_value: Hash to verify against
            salt: Salt used in hashing

        Returns:
            bool: True if hash matches
        """
        new_hash, _ = SecurityExamples.hash_data(data, salt)
        return hmac.compare_digest(new_hash, hash_value)

    # ============================================================================
    # RATE LIMITING
    # ============================================================================

    class RateLimiter:
        """Simple in-memory rate limiter."""

        def __init__(self, max_requests: int, window_seconds: int):
            self.max_requests = max_requests
            self.window_seconds = window_seconds
            self.requests: Dict[str, list[datetime]] = {}

        def is_allowed(self, identifier: str) -> bool:
            """
            Check if request is allowed.

            Args:
                identifier: Unique identifier (e.g., IP address, user ID)

            Returns:
                bool: True if allowed, False if rate limit exceeded
            """
            now = datetime.utcnow()
            window_start = now - timedelta(seconds=self.window_seconds)

            # Initialize or clean old requests
            if identifier not in self.requests:
                self.requests[identifier] = []

            # Remove old requests
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > window_start
            ]

            # Check limit
            if len(self.requests[identifier]) >= self.max_requests:
                return False

            # Add current request
            self.requests[identifier].append(now)
            return True

    # ============================================================================
    # IP ADDRESS VALIDATION
    # ============================================================================

    @staticmethod
    def validate_ip_address(ip: str) -> bool:
        """
        Validate IP address format.

        Args:
            ip: IP address to validate

        Returns:
            bool: True if valid IPv4 or IPv6
        """
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_private_ip(ip: str) -> bool:
        """
        Check if IP address is private.

        Args:
            ip: IP address to check

        Returns:
            bool: True if private
        """
        try:
            ip_obj = ipaddress.ip_address(ip)
            return ip_obj.is_private
        except ValueError:
            return False

    # ============================================================================
    # SQL INJECTION PREVENTION
    # ============================================================================

    @staticmethod
    def demonstrate_sql_injection_prevention():
        """
        Demonstrate SQL injection prevention.

        BAD (Vulnerable to SQL injection):
        query = f"SELECT * FROM users WHERE username = '{username}'"

        GOOD (Using parameterized queries with SQLAlchemy):
        query = db.query(User).filter(User.username == username)

        The ORM automatically handles parameterization.
        """
        examples = {
            "vulnerable": "SELECT * FROM users WHERE username = '{}'",
            "safe_orm": "db.query(User).filter(User.username == username)",
            "safe_raw": "SELECT * FROM users WHERE username = %s (with params)",
        }
        return examples

    # ============================================================================
    # CSRF PROTECTION
    # ============================================================================

    @staticmethod
    def generate_csrf_token() -> str:
        """
        Generate CSRF token.

        Returns:
            str: CSRF token
        """
        return secrets.token_urlsafe(32)

    @staticmethod
    def verify_csrf_token(token: str, expected_token: str) -> bool:
        """
        Verify CSRF token.

        Args:
            token: Token from request
            expected_token: Expected token

        Returns:
            bool: True if tokens match
        """
        return hmac.compare_digest(token, expected_token)

    # ============================================================================
    # SECURE HEADERS
    # ============================================================================

    @staticmethod
    def get_security_headers() -> Dict[str, str]:
        """
        Get recommended security headers.

        Returns:
            dict: Security headers
        """
        return {
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
        }

    # ============================================================================
    # PASSWORD POLICY
    # ============================================================================

    @staticmethod
    def check_password_complexity(password: str) -> Dict[str, Any]:
        """
        Check password complexity and return detailed feedback.

        Args:
            password: Password to check

        Returns:
            dict: Complexity analysis
        """
        checks = {
            "length": len(password) >= 8,
            "uppercase": bool(re.search(r'[A-Z]', password)),
            "lowercase": bool(re.search(r'[a-z]', password)),
            "digit": bool(re.search(r'\d', password)),
            "special": bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password)),
            "no_common": password.lower() not in [
                "password", "12345678", "qwerty", "admin", "letmein"
            ]
        }

        score = sum(checks.values())
        strength = "weak"
        if score >= 5:
            strength = "strong"
        elif score >= 4:
            strength = "medium"

        return {
            "checks": checks,
            "score": score,
            "strength": strength,
            "is_valid": all(checks.values())
        }

    # ============================================================================
    # SESSION MANAGEMENT
    # ============================================================================

    @staticmethod
    def generate_session_id() -> str:
        """
        Generate secure session ID.

        Returns:
            str: Session ID
        """
        return secrets.token_urlsafe(64)

    # ============================================================================
    # TIMING ATTACK PREVENTION
    # ============================================================================

    @staticmethod
    def constant_time_compare(a: str, b: str) -> bool:
        """
        Compare strings in constant time to prevent timing attacks.

        Args:
            a: First string
            b: Second string

        Returns:
            bool: True if strings match
        """
        return hmac.compare_digest(a, b)


# Example usage and demonstrations
def security_examples_demo():
    """Demonstrate security examples."""

    print("=== Security Examples Demo ===\n")

    # Email validation
    print("1. Email Validation:")
    test_emails = ["test@example.com", "invalid.email", "user@domain"]
    for email in test_emails:
        valid = SecurityExamples.validate_email(email)
        print(f"  {email}: {'✓ Valid' if valid else '✗ Invalid'}")

    print("\n2. Password Complexity:")
    test_passwords = ["weak", "StrongPass123!", "12345678"]
    for pwd in test_passwords:
        result = SecurityExamples.check_password_complexity(pwd)
        print(f"  {pwd}: {result['strength']} (score: {result['score']}/6)")

    print("\n3. Secure Token Generation:")
    token = SecurityExamples.generate_secure_token()
    print(f"  Generated token: {token}")

    print("\n4. Security Headers:")
    headers = SecurityExamples.get_security_headers()
    for key, value in headers.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    security_examples_demo()
