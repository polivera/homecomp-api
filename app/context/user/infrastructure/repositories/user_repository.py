from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.context.user.domain.contracts.infrastrutcure import UserRepositoryContract
from app.context.user.domain.dto import UserDTO
from app.context.user.domain.value_objects import Email


class UserRepository(UserRepositoryContract):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def find_user(self, email: Optional[Email]) -> Optional[UserDTO]:
        print(email)
        return UserDTO(email=Email(value="test@test.com"))
