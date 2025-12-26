from app.context.user_account.application.contracts.find_accounts_by_user_handler_contract import (
    FindAccountsByUserHandlerContract,
)
from app.context.user_account.application.dto.account_response_dto import (
    AccountResponseDTO,
)
from app.context.user_account.application.queries.find_accounts_by_user_query import (
    FindAccountsByUserQuery,
)
from app.context.user_account.domain.contracts.infrastructure.user_account_repository_contract import (
    UserAccountRepositoryContract,
)


class FindAccountsByUserHandler(FindAccountsByUserHandlerContract):
    def __init__(self, repository: UserAccountRepositoryContract):
        self._repository = repository

    async def handle(self, query: FindAccountsByUserQuery) -> list[AccountResponseDTO]:
        accounts = await self._repository.find_accounts_by_user(user_id=query.user_id)
        return [AccountResponseDTO.from_domain_dto(acc) for acc in accounts]
