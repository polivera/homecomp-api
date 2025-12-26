from datetime import datetime
from typing import Optional

from sqlalchemy import select, update
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
        stmt = select(UserAccountModel).where(UserAccountModel.deleted_at.is_(None))

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

    async def find_accounts_by_user(self, user_id: UserID) -> list[UserAccountDTO]:
        """Find all non-deleted accounts for a user"""
        stmt = select(UserAccountModel).where(
            UserAccountModel.user_id == user_id.value,
            UserAccountModel.deleted_at.is_(None)
        )
        result = await self._db.execute(stmt)
        models = result.scalars().all()
        return [UserAccountMapper.toDTO(model) for model in models]

    async def update_account(self, account: UserAccountDTO) -> UserAccountDTO:
        """Update an existing account"""
        stmt = (
            update(UserAccountModel)
            .where(
                UserAccountModel.id == account.account_id.value,
                UserAccountModel.deleted_at.is_(None)
            )
            .values(
                name=account.name.value,
                currency=account.currency.value,
                balance=account.balance.value
            )
        )

        result = await self._db.execute(stmt)
        if result.rowcount == 0:
            raise ValueError("Account not found or already deleted")

        await self._db.commit()

        # Fetch updated record
        updated = await self.find_account(account_id=account.account_id)
        return updated

    async def delete_account(self, account_id: AccountID, user_id: UserID) -> bool:
        """Soft delete an account"""
        # Verify account exists and user owns it
        account = await self.find_account(account_id=account_id)
        if not account or account.user_id.value != user_id.value:
            return False

        # Soft delete: set deleted_at timestamp
        stmt = (
            update(UserAccountModel)
            .where(
                UserAccountModel.id == account_id.value,
                UserAccountModel.user_id == user_id.value,
                UserAccountModel.deleted_at.is_(None)
            )
            .values(deleted_at=datetime.utcnow())
        )

        result = await self._db.execute(stmt)
        await self._db.commit()

        return result.rowcount > 0
