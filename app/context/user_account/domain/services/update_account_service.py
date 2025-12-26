from app.context.user.domain.value_objects.user_id import UserID
from app.context.user_account.domain.contracts.infrastructure.user_account_repository_contract import (
    UserAccountRepositoryContract,
)
from app.context.user_account.domain.contracts.services.update_account_service_contract import (
    UpdateAccountServiceContract,
)
from app.context.user_account.domain.dto.user_account_dto import UserAccountDTO
from app.context.user_account.domain.value_objects.account_id import AccountID
from app.context.user_account.domain.value_objects.account_name import AccountName
from app.context.user_account.domain.value_objects.balance import Balance
from app.context.user_account.domain.value_objects.currency import Currency


class UpdateAccountService(UpdateAccountServiceContract):
    def __init__(self, repository: UserAccountRepositoryContract):
        self._repository = repository

    async def update_account(
        self,
        account_id: AccountID,
        user_id: UserID,
        name: AccountName,
        currency: Currency,
        balance: Balance,
    ) -> UserAccountDTO:
        # 1. Check account exists and user owns it
        existing = await self._repository.find_account(account_id=account_id)
        if not existing:
            raise ValueError("Account not found")
        if existing.user_id.value != user_id.value:
            raise ValueError("Account not found")  # Don't reveal it exists

        # 2. If name changed, check for duplicates
        if existing.name.value != name.value:
            duplicate = await self._repository.find_account(user_id=user_id, name=name)
            if duplicate and duplicate.account_id.value != account_id.value:
                raise ValueError(f"Account with name '{name.value}' already exists")

        # 3. Update account
        updated_dto = UserAccountDTO(
            account_id=account_id,
            user_id=user_id,
            name=name,
            currency=currency,
            balance=balance,
        )
        return await self._repository.update_account(updated_dto)
