from abc import ABC, abstractmethod

from app.context.user_account.application.dto.account_response_dto import (
    AccountResponseDTO,
)
from app.context.user_account.application.queries.find_accounts_by_user_query import (
    FindAccountsByUserQuery,
)


class FindAccountsByUserHandlerContract(ABC):
    @abstractmethod
    async def handle(self, query: FindAccountsByUserQuery) -> list[AccountResponseDTO]:
        pass
