from fastapi import APIRouter, Depends, HTTPException, status
from app.context.auth.application.services.user_service import UserService
from app.context.auth.interface.rest.dependencies import get_user_service
from app.context.auth.interface.rest.schemas import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from typing import List

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    """
    Get user by ID.

    Notice how clean this is! We inject UserService directly,
    and FastAPI handles the entire dependency chain:
    get_db() → get_user_repository() → get_user_service()
    """
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
):
    """
    Create a new user.

    The same dependency injection chain happens here automatically.
    """
    return await user_service.create_user(
        email=user_data.email,
        username=user_data.username,
        password=user_data.password,
    )


@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service),
):
    """List all users with pagination"""
    return await user_service.list_users(skip, limit)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    """Update user information"""
    return await user_service.update_user(
        user_id=user_id,
        email=user_data.email,
        username=user_data.username,
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
):
    """Delete a user"""
    await user_service.delete_user(user_id)
    return None
