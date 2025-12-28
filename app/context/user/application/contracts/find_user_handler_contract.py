from abc import ABC, abstractmethod
from typing import Optional

from app.context.user.application.dto import UserContextDTO
from app.context.user.application.queries import FindUserQuery


class FindUserHandlerContract(ABC):
    @abstractmethod
    async def handle(self, query: FindUserQuery) -> Optional[UserContextDTO]:
        pass
