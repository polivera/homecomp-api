from abc import ABC, abstractmethod

from app.context.auth.application.query import GetSessionQuery


class GetSessionHandlerContract(ABC):
    @abstractmethod
    async def handle(self, query: GetSessionQuery):
        pass
