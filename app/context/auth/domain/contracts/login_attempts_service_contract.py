from abc import ABC, abstractmethod

from app.context.user.domain.value_objects import UserEmail


class LoginAttemptsServiceContract(ABC):
    @abstractmethod
    async def handle(self, email: UserEmail):
        pass
