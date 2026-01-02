from abc import ABC, abstractmethod

from app.context.user_account.application.dto.find_single_account_result import FindSingleAccountResult
from app.context.user_account.application.queries.find_account_by_id_query import (
    FindAccountByIdQuery,
)


class FindAccountByIdHandlerContract(ABC):
    @abstractmethod
    async def handle(self, query: FindAccountByIdQuery) -> FindSingleAccountResult:
        pass
