from abc import ABC, abstractmethod

from app.context.auth.domain.value_objects import AuthEmail, AuthPassword


class LoginServiceContract(ABC):
    @abstractmethod
    async def handle(self, email: AuthEmail, plain_password: AuthPassword):
        pass
