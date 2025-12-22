from abc import ABC, abstractmethod

from app.context.auth.domain.dto import AuthUserDTO
from app.context.auth.domain.value_objects import AuthPassword


class LoginServiceContract(ABC):
    @abstractmethod
    async def handle(self, user_password: AuthPassword, db_user: AuthUserDTO):
        pass
