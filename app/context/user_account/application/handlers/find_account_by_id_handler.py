from app.context.user_account.application.contracts.find_account_by_id_handler_contract import (
    FindAccountByIdHandlerContract,
)
from app.context.user_account.application.dto.account_response_dto import (
    AccountResponseDTO,
)
from app.context.user_account.application.dto.find_single_account_result import (
    FindSingleAccountErrorCode,
    FindSingleAccountResult,
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
from app.shared.domain.contracts import LoggerContract


class FindAccountByIdHandler(FindAccountByIdHandlerContract):
    def __init__(self, repository: UserAccountRepositoryContract, logger: LoggerContract):
        self._repository = repository
        self._logger = logger

    async def handle(self, query: FindAccountByIdQuery) -> FindSingleAccountResult:
        account = await self._repository.find_user_accounts(
            account_id=UserAccountID(query.account_id),
            user_id=UserAccountUserID(query.user_id),
        )

        if not account or account.__len__() < 1:
            return FindSingleAccountResult(
                error_code=FindSingleAccountErrorCode.NOT_FOUND, error_message="No account found"
            )

        return FindSingleAccountResult(account=AccountResponseDTO.from_domain_dto(account[0]))
