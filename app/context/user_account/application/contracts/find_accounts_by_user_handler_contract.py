from abc import ABC, abstractmethod

from app.context.user_account.application.dto.find_multiple_accounts_result import (
    FindMultipleAccountsResult,
)
from app.context.user_account.application.queries.find_accounts_by_user_query import (
    FindAccountsByUserQuery,
)


class FindAccountsByUserHandlerContract(ABC):
    @abstractmethod
    async def handle(self, query: FindAccountsByUserQuery) -> FindMultipleAccountsResult:
        pass
