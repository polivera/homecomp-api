from app.context.user_account.application.contracts.find_accounts_by_user_handler_contract import (
    FindAccountsByUserHandlerContract,
)
from app.context.user_account.application.dto import AccountResponseDTO
from app.context.user_account.application.dto.find_multiple_accounts_result import (
    FindMultipleAccountsErrorCode,
    FindMultipleAccountsResult,
)
from app.context.user_account.application.queries.find_accounts_by_user_query import (
    FindAccountsByUserQuery,
)
from app.context.user_account.domain.contracts.infrastructure.user_account_repository_contract import (
    UserAccountRepositoryContract,
)
from app.context.user_account.domain.value_objects import UserAccountUserID


class FindAccountsByUserHandler(FindAccountsByUserHandlerContract):
    def __init__(self, repository: UserAccountRepositoryContract):
        self._repository = repository

    async def handle(self, query: FindAccountsByUserQuery) -> FindMultipleAccountsResult:
        try:
            accounts = await self._repository.find_user_accounts(user_id=UserAccountUserID(query.user_id))

            if accounts is None:
                return FindMultipleAccountsResult(accounts=[])

            account_dtos = [AccountResponseDTO.from_domain_dto(acc) for acc in accounts]
            return FindMultipleAccountsResult(accounts=account_dtos)

        except Exception:
            return FindMultipleAccountsResult(
                error_code=FindMultipleAccountsErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error while finding accounts",
            )
