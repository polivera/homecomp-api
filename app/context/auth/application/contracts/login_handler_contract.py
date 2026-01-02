from abc import ABC, abstractmethod

from app.context.auth.application.commands import LoginCommand
from app.context.auth.application.dto import LoginHandlerResultDTO


class LoginHandlerContract(ABC):
    @abstractmethod
    async def handle(self, command: LoginCommand) -> LoginHandlerResultDTO:
        pass
