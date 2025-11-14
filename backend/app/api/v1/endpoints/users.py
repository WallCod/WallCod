"""
User management endpoints.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ....core.database import get_db
from ....core.security import get_current_user_id
from ....schemas.user import UserResponse, UserUpdate
from ....services.user_service import UserService


router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get list of users.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session

    Returns:
        List[UserResponse]: List of users
    """
    users = UserService.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get user by ID.

    Args:
        user_id: User ID
        db: Database session

    Returns:
        UserResponse: User data

    Raises:
        HTTPException: If user not found
    """
    user = UserService.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Update user profile.

    Args:
        user_id: User ID
        user_data: User update data
        current_user_id: Current user ID from token
        db: Database session

    Returns:
        UserResponse: Updated user data

    Raises:
        HTTPException: If user not found or unauthorized
    """
    # Check if user is updating their own profile
    if int(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )

    user = UserService.update_user(db, user_id, user_data)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Delete user account.

    Args:
        user_id: User ID
        current_user_id: Current user ID from token
        db: Database session

    Raises:
        HTTPException: If user not found or unauthorized
    """
    # Check if user is deleting their own account
    if int(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )

    UserService.delete_user(db, user_id)
    return None
