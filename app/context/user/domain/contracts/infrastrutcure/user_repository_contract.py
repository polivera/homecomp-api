from abc import ABC, abstractmethod
from typing import Optional

from app.context.user.domain.dto import UserDTO
from app.context.user.domain.value_objects import Email


class UserRepositoryContract(ABC):
    @abstractmethod
    async def find_user(self, email: Optional[Email]) -> Optional[UserDTO]:
        pass
