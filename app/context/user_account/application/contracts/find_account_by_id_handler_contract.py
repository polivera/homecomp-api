from abc import ABC, abstractmethod
from typing import Optional

from app.context.user_account.application.dto.account_response_dto import (
    AccountResponseDTO,
)
from app.context.user_account.application.queries.find_account_by_id_query import (
    FindAccountByIdQuery,
)


class FindAccountByIdHandlerContract(ABC):
    @abstractmethod
    async def handle(
        self, query: FindAccountByIdQuery
    ) -> Optional[AccountResponseDTO]:
        pass
