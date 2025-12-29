
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.user.domain.contracts.infrastructure import UserRepositoryContract
from app.context.user.domain.dto import UserDTO
from app.context.user.domain.value_objects import UserEmail, UserID
from app.context.user.infrastructure.mappers import UserMapper
from app.context.user.infrastructure.models import UserModel


class UserRepository(UserRepositoryContract):
    """Repository implementation for User aggregate"""

    def __init__(self, db: AsyncSession):
        self._db = db

    async def find_user(
        self, user_id: UserID | None = None, email: UserEmail | None = None
    ) -> UserDTO | None:
        """
        Find a user by ID or email.
        Both filters can be applied simultaneously.
        """
        stmt = select(UserModel)

        if user_id is not None:
            stmt = stmt.where(UserModel.id == user_id.value)
        if email is not None:
            stmt = stmt.where(UserModel.email == email.value)

        result = await self._db.execute(stmt)
        return UserMapper.to_dto(result.scalar_one_or_none())
