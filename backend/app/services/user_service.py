"""
User service layer for business logic.
"""
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from ..core.security import get_password_hash, verify_password


class UserService:
    """Service class for user operations."""

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username."""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get list of users."""
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        Create a new user.

        Args:
            db: Database session
            user_data: User creation data

        Returns:
            User: The created user

        Raises:
            HTTPException: If user already exists
        """
        # Check if user already exists
        if UserService.get_user_by_email(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        if UserService.get_user_by_username(db, user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        # Create new user
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=get_password_hash(user_data.password),
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
        """
        Update user profile.

        Args:
            db: Database session
            user_id: User ID
            user_data: User update data

        Returns:
            User: The updated user

        Raises:
            HTTPException: If user not found
        """
        db_user = UserService.get_user_by_id(db, user_id)

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Update user fields
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """
        Delete user.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            bool: True if deleted successfully

        Raises:
            HTTPException: If user not found
        """
        db_user = UserService.get_user_by_id(db, user_id)

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        db.delete(db_user)
        db.commit()

        return True

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """
        Authenticate user with username/email and password.

        Args:
            db: Database session
            username: Username or email
            password: Plain text password

        Returns:
            User: The authenticated user or None
        """
        # Try to get user by username or email
        user = UserService.get_user_by_username(db, username)
        if not user:
            user = UserService.get_user_by_email(db, username)

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()

        return user

    @staticmethod
    def activate_user(db: Session, user_id: int) -> User:
        """Activate user account."""
        user = UserService.get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user.is_active = True
        user.is_verified = True
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def deactivate_user(db: Session, user_id: int) -> User:
        """Deactivate user account."""
        user = UserService.get_user_by_id(db, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user.is_active = False
        db.commit()
        db.refresh(user)

        return user
