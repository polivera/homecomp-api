from abc import ABC, abstractmethod
from typing import Optional
from app.context.user.application.query import FindUserQuery
from app.context.user.application.dto import UserContextDTO


class FindUserHandlerContract(ABC):
    @abstractmethod
    async def handle(self, query: FindUserQuery) -> Optional[UserContextDTO]:
        pass
