from abc import ABC, abstractmethod
from typing import Optional

from app.context.user.domain.dto import UserDTO
from app.context.user.domain.value_objects import Email, UserID


class UserRepositoryContract(ABC):
    @abstractmethod
    async def find_user(
        self, user_id: Optional[UserID] = None, email: Optional[Email] = None
    ) -> Optional[UserDTO]:
        pass
