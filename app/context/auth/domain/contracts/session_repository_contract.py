from abc import ABC, abstractmethod

from app.context.auth.domain.value_objects import FailedLoginAttempts
from app.context.user.domain.value_objects import Email


class SessionRepositoryContract(ABC):
    @abstractmethod
    async def getLoginAttepmts(self, email: Email) -> FailedLoginAttempts:
        pass

    async def updateAttempts(self, email: Email, attempts: FailedLoginAttempts) -> None:
        pass

    async def clearAttempts(self, email: Email) -> None:
        pass
