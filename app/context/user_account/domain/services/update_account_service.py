from app.context.user_account.domain.contracts.infrastructure import (
    UserAccountRepositoryContract,
)
from app.context.user_account.domain.contracts.services import (
    UpdateAccountServiceContract,
)
from app.context.user_account.domain.dto import UserAccountDTO
from app.context.user_account.domain.value_objects import (
    AccountName,
    UserAccountBalance,
    UserAccountCurrency,
    UserAccountID,
    UserAccountUserID,
)


class UpdateAccountService(UpdateAccountServiceContract):
    def __init__(self, repository: UserAccountRepositoryContract):
        self._repository = repository

    async def update_account(
        self,
        account_id: UserAccountID,
        user_id: UserAccountUserID,
        name: AccountName,
        currency: UserAccountCurrency,
        balance: UserAccountBalance,
    ) -> UserAccountDTO:
        existing = await self._repository.find_user_accounts(
            user_id=user_id, account_id=account_id
        )

        if not existing:
            raise ValueError("Account not found")

        # FIX: find_user_accounts use like instead of equal, error prone on this check
        if existing.name.value != name.value:
            # In this case, we should also search inactive for name repetition
            duplicate = await self._repository.find_user_accounts(
                user_id=user_id, name=name, only_active=False
            )
            if (
                duplicate
                and duplicate.account_id
                and duplicate.account_id.value != account_id.value
            ):
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
