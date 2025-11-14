"""
Authentication endpoints.
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....core.security import (
    create_access_token,
    create_refresh_token,
    get_current_user_id,
)
from ....core.config import settings
from ....schemas.user import Token, UserCreate, UserResponse
from ....services.user_service import UserService


router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new user.

    Args:
        user_data: User registration data
        db: Database session

    Returns:
        UserResponse: The created user

    Raises:
        HTTPException: If registration is disabled or user already exists
    """
    if not settings.ENABLE_REGISTRATION:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Registration is currently disabled"
        )

    user = UserService.create_user(db, user_data)
    return user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login and get access token.

    Args:
        form_data: OAuth2 form with username and password
        db: Database session

    Returns:
        Token: Access and refresh tokens

    Raises:
        HTTPException: If credentials are invalid
    """
    user = UserService.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Refresh access token.

    Args:
        current_user_id: Current user ID from token
        db: Database session

    Returns:
        Token: New access and refresh tokens

    Raises:
        HTTPException: If user not found or inactive
    """
    user = UserService.get_user_by_id(db, int(current_user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Create new tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Get current user profile.

    Args:
        current_user_id: Current user ID from token
        db: Database session

    Returns:
        UserResponse: Current user data

    Raises:
        HTTPException: If user not found
    """
    user = UserService.get_user_by_id(db, int(current_user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user
