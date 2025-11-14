"""
Tests for user endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..main import app
from ..core.database import Base, get_db
from ..models.user import User
from ..core.security import get_password_hash


# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Set up test database."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestUserRegistration:
    """Test user registration."""

    def test_register_user(self):
        """Test successful user registration."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "TestPassword123!",
                "full_name": "Test User"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert "id" in data

    def test_register_duplicate_email(self):
        """Test registration with duplicate email."""
        # First registration
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser1",
                "password": "TestPassword123!"
            }
        )

        # Second registration with same email
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser2",
                "password": "TestPassword123!"
            }
        )

        assert response.status_code == 400
        assert "Email already registered" in response.json()["detail"]

    def test_register_duplicate_username(self):
        """Test registration with duplicate username."""
        # First registration
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test1@example.com",
                "username": "testuser",
                "password": "TestPassword123!"
            }
        )

        # Second registration with same username
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test2@example.com",
                "username": "testuser",
                "password": "TestPassword123!"
            }
        )

        assert response.status_code == 400
        assert "Username already taken" in response.json()["detail"]

    def test_register_weak_password(self):
        """Test registration with weak password."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "weak"
            }
        )

        assert response.status_code == 422


class TestUserLogin:
    """Test user login."""

    def test_login_success(self):
        """Test successful login."""
        # Register user first
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "TestPassword123!"
            }
        )

        # Login
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "testuser",
                "password": "TestPassword123!"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self):
        """Test login with wrong password."""
        # Register user first
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "TestPassword123!"
            }
        )

        # Login with wrong password
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "testuser",
                "password": "WrongPassword123!"
            }
        )

        assert response.status_code == 401

    def test_login_nonexistent_user(self):
        """Test login with nonexistent user."""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "nonexistent",
                "password": "TestPassword123!"
            }
        )

        assert response.status_code == 401


class TestUserProfile:
    """Test user profile endpoints."""

    def get_auth_headers(self):
        """Helper to get authentication headers."""
        # Register and login
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "TestPassword123!"
            }
        )

        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "testuser",
                "password": "TestPassword123!"
            }
        )

        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    def test_get_current_user(self):
        """Test getting current user profile."""
        headers = self.get_auth_headers()

        response = client.get("/api/v1/auth/me", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"

    def test_get_current_user_unauthorized(self):
        """Test getting current user without authentication."""
        response = client.get("/api/v1/auth/me")

        assert response.status_code == 401
