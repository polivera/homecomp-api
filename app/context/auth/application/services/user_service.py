from app.context.auth.infrastructure.repositories.user_repository import UserRepository
from app.context.auth.domain.models.user import User
from typing import Optional, List
from fastapi import HTTPException


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return await self.user_repo.find_by_id(user_id)

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return await self.user_repo.find_by_email(email)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        return await self.user_repo.find_by_username(username)

    async def create_user(
        self, email: str, username: str, password: str
    ) -> User:
        """
        Create a new user

        Note: In production, you should hash the password using a library like bcrypt or passlib
        """
        # Check if user already exists
        existing_user = await self.user_repo.find_by_email(email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        existing_username = await self.user_repo.find_by_username(username)
        if existing_username:
            raise HTTPException(status_code=400, detail="Username already taken")

        # TODO: Hash password before storing
        # from passlib.context import CryptContext
        # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        # hashed_password = pwd_context.hash(password)

        user = User(
            email=email,
            username=username,
            hashed_password=password,  # WARNING: Should be hashed in production!
        )
        return await self.user_repo.create(user)

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """List all users with pagination"""
        return await self.user_repo.list_all(skip, limit)

    async def update_user(
        self,
        user_id: int,
        email: Optional[str] = None,
        username: Optional[str] = None,
    ) -> User:
        """Update user information"""
        user = await self.user_repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if email:
            existing = await self.user_repo.find_by_email(email)
            if existing and existing.id != user_id:
                raise HTTPException(status_code=400, detail="Email already in use")
            user.email = email

        if username:
            existing = await self.user_repo.find_by_username(username)
            if existing and existing.id != user_id:
                raise HTTPException(status_code=400, detail="Username already taken")
            user.username = username

        return await self.user_repo.update(user)

    async def delete_user(self, user_id: int) -> None:
        """Delete a user"""
        user = await self.user_repo.find_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        await self.user_repo.delete(user)
