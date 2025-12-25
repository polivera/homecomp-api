from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.user.domain.value_objects.user_id import UserID
from app.context.user_account.domain.contracts.infrastructure.user_account_repository_contract import (
    UserAccountRepositoryContract,
)
from app.context.user_account.domain.dto.user_account_dto import UserAccountDTO
from app.context.user_account.domain.value_objects.account_id import AccountID
from app.context.user_account.domain.value_objects.account_name import AccountName
from app.context.user_account.infrastructure.mappers.user_account_mapper import (
    UserAccountMapper,
)
from app.context.user_account.infrastructure.models.user_account_model import (
    UserAccountModel,
)


class UserAccountRepository(UserAccountRepositoryContract):
    """Repository implementation for user account operations"""

    def __init__(self, db: AsyncSession):
        self._db = db

    async def save_account(self, account: UserAccountDTO) -> UserAccountDTO:
        """Create a new user account"""
        # Convert DTO to model (without ID for new records)
        model = UserAccountModel(
            user_id=account.user_id.value,
            name=account.name.value,
            currency=account.currency.value,
            balance=account.balance.value,
        )

        self._db.add(model)

        try:
            await self._db.commit()
            await self._db.refresh(model)
        except IntegrityError as e:
            await self._db.rollback()
            raise ValueError(
                f"Account with name '{account.name.value}' already exists for this user"
            ) from e

        return UserAccountMapper.toDTO(model)

    async def find_account(
        self,
        account_id: Optional[AccountID] = None,
        user_id: Optional[UserID] = None,
        name: Optional[AccountName] = None,
    ) -> Optional[UserAccountDTO]:
        """Find an account by ID or by user_id and name"""
        stmt = select(UserAccountModel)

        if account_id is not None:
            stmt = stmt.where(UserAccountModel.id == account_id.value)
        elif user_id is not None and name is not None:
            stmt = stmt.where(
                UserAccountModel.user_id == user_id.value,
                UserAccountModel.name == name.value,
            )
        else:
            raise ValueError("Must provide either account_id or both user_id and name")

        result = await self._db.execute(stmt)
        model = result.scalar_one_or_none()

        return UserAccountMapper.toDTO(model) if model else None
