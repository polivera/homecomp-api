from typing import Optional

from app.context.user_account.application.contracts.find_account_by_id_handler_contract import (
    FindAccountByIdHandlerContract,
)
from app.context.user_account.application.dto.account_response_dto import (
    AccountResponseDTO,
)
from app.context.user_account.application.queries.find_account_by_id_query import (
    FindAccountByIdQuery,
)
from app.context.user_account.domain.contracts.infrastructure.user_account_repository_contract import (
    UserAccountRepositoryContract,
)
from app.context.user_account.domain.value_objects import (
    UserAccountID,
    UserAccountUserID,
)


class FindAccountByIdHandler(FindAccountByIdHandlerContract):
    def __init__(self, repository: UserAccountRepositoryContract):
        self._repository = repository

    async def handle(self, query: FindAccountByIdQuery) -> Optional[AccountResponseDTO]:
        account = await self._repository.find_user_accounts(
            account_id=UserAccountID(query.account_id),
            user_id=UserAccountUserID(query.user_id),
        )

        return AccountResponseDTO.from_domain_dto(account) if account else None
