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


class FindAccountByIdHandler(FindAccountByIdHandlerContract):
    def __init__(self, repository: UserAccountRepositoryContract):
        self._repository = repository

    async def handle(self, query: FindAccountByIdQuery) -> Optional[AccountResponseDTO]:
        # Call repository directly (CQRS - queries bypass domain)
        account = await self._repository.find_account(account_id=query.account_id)

        # Authorization: verify user owns the account
        if account and account.user_id.value != query.user_id.value:
            return None  # Return 404, not 403

        return AccountResponseDTO.from_domain_dto(account) if account else None
