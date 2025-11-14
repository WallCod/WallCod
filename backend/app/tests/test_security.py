"""
Tests for security utilities.
"""
import pytest
from datetime import datetime, timedelta
from jose import jwt
from ..core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    validate_password_strength,
    sanitize_input,
)
from ..core.config import settings


class TestPasswordHashing:
    """Test password hashing functions."""

    def test_password_hash_and_verify(self):
        """Test password hashing and verification."""
        password = "TestPassword123!"
        hashed = get_password_hash(password)

        assert hashed != password
        assert verify_password(password, hashed)

    def test_wrong_password(self):
        """Test verification with wrong password."""
        password = "TestPassword123!"
        wrong_password = "WrongPassword456!"
        hashed = get_password_hash(password)

        assert not verify_password(wrong_password, hashed)


class TestTokens:
    """Test JWT token functions."""

    def test_create_access_token(self):
        """Test access token creation."""
        data = {"sub": "123"}
        token = create_access_token(data)

        assert token is not None
        assert isinstance(token, str)

    def test_create_refresh_token(self):
        """Test refresh token creation."""
        data = {"sub": "123"}
        token = create_refresh_token(data)

        assert token is not None
        assert isinstance(token, str)

    def test_decode_valid_token(self):
        """Test decoding valid token."""
        data = {"sub": "123"}
        token = create_access_token(data)
        payload = decode_token(token)

        assert payload["sub"] == "123"
        assert "exp" in payload
        assert "iat" in payload
        assert payload["type"] == "access"

    def test_decode_expired_token(self):
        """Test decoding expired token."""
        data = {"sub": "123"}
        expires_delta = timedelta(seconds=-1)  # Already expired
        token = create_access_token(data, expires_delta)

        with pytest.raises(Exception):
            decode_token(token)


class TestPasswordValidation:
    """Test password strength validation."""

    def test_valid_password(self):
        """Test valid password."""
        assert validate_password_strength("SecurePass123!")

    def test_short_password(self):
        """Test password too short."""
        with pytest.raises(ValueError, match="at least 8 characters"):
            validate_password_strength("Short1!")

    def test_no_uppercase(self):
        """Test password without uppercase."""
        with pytest.raises(ValueError, match="uppercase letter"):
            validate_password_strength("lowercase123!")

    def test_no_lowercase(self):
        """Test password without lowercase."""
        with pytest.raises(ValueError, match="lowercase letter"):
            validate_password_strength("UPPERCASE123!")

    def test_no_digit(self):
        """Test password without digit."""
        with pytest.raises(ValueError, match="digit"):
            validate_password_strength("NoDigitPass!")

    def test_no_special_char(self):
        """Test password without special character."""
        with pytest.raises(ValueError, match="special character"):
            validate_password_strength("NoSpecial123")


class TestInputSanitization:
    """Test input sanitization."""

    def test_sanitize_normal_input(self):
        """Test sanitization of normal input."""
        input_str = "Hello World"
        result = sanitize_input(input_str)
        assert result == "Hello World"

    def test_sanitize_with_null_bytes(self):
        """Test sanitization removes null bytes."""
        input_str = "Hello\x00World"
        result = sanitize_input(input_str)
        assert "\x00" not in result
        assert result == "HelloWorld"

    def test_sanitize_with_control_chars(self):
        """Test sanitization removes control characters."""
        input_str = "Hello\x01\x02World"
        result = sanitize_input(input_str)
        assert result == "HelloWorld"

    def test_sanitize_with_whitespace(self):
        """Test sanitization preserves allowed whitespace."""
        input_str = "  Hello\nWorld\t  "
        result = sanitize_input(input_str)
        assert result == "Hello\nWorld"
