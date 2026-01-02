from abc import ABC, abstractmethod

from app.context.auth.application.dto.get_session_result_dto import GetSessionResultDTO
from app.context.auth.application.queries import GetSessionQuery


class GetSessionHandlerContract(ABC):
    @abstractmethod
    async def handle(self, query: GetSessionQuery) -> GetSessionResultDTO | None:
        pass
