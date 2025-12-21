from abc import ABC, abstractmethod

from app.context.user.domain.value_objects import Email


class LoginAttemptsServiceContract(ABC):
    @abstractmethod
    async def handle(self, email: Email):
        pass
