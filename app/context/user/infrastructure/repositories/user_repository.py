from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.user.domain.contracts.infrastrutcure import UserRepositoryContract
from app.context.user.domain.dto import UserDTO
from app.context.user.domain.value_objects import Email, UserID
from app.context.user.infrastructure.mappers import UserMapper
from app.context.user.infrastructure.models import UserModel


class UserRepository(UserRepositoryContract):
    _db: AsyncSession

    def __init__(self, db: AsyncSession):
        self._db = db

    async def find_user(
        self, user_id: Optional[UserID] = None, email: Optional[Email] = None
    ) -> Optional[UserDTO]:
        stmt = select(UserModel)

        if user_id is not None:
            stmt = stmt.where(UserModel.id == user_id.value)
        else:
            if email is not None:
                stmt = stmt.where(UserModel.email == email.value)

        res = await self._db.execute(stmt)

        return UserMapper.toDTO(res.scalar_one_or_none())
