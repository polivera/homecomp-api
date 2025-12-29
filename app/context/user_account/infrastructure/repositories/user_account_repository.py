from typing import Any, cast

from sqlalchemy import select, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.user_account.domain.contracts.infrastructure import (
    UserAccountRepositoryContract,
)
from app.context.user_account.domain.dto import UserAccountDTO
from app.context.user_account.domain.exceptions import (
    UserAccountNameAlreadyExistError,
    UserAccountNotFoundError,
)
from app.context.user_account.domain.value_objects import (
    AccountName,
    UserAccountDeletedAt,
    UserAccountID,
    UserAccountUserID,
)
from app.context.user_account.infrastructure.mappers import (
    UserAccountMapper,
)
from app.context.user_account.infrastructure.models import (
    UserAccountModel,
)


class UserAccountRepository(UserAccountRepositoryContract):
    """Repository implementation for user account operations"""

    def __init__(self, db: AsyncSession):
        self._db = db

    async def save_account(self, account: UserAccountDTO) -> UserAccountDTO:
        """Create a new user account"""
        model = UserAccountMapper.to_model(account)
        self._db.add(model)
        try:
            await self._db.commit()
            await self._db.refresh(model)
        except IntegrityError as e:
            await self._db.rollback()
            raise UserAccountNameAlreadyExistError(
                f"Account with name '{account.name.value}' already exists for this user"
            ) from e

        return UserAccountMapper.to_dto_or_fail(model)

    async def find_account(
        self,
        account_id: UserAccountID | None = None,
        user_id: UserAccountUserID | None = None,
        name: AccountName | None = None,
        only_active: bool | None = True,
    ) -> UserAccountDTO | None:
        """Find an account by ID or by user_id and name (admin/unrestricted usage)"""
        stmt = select(UserAccountModel)
        if only_active:
            stmt = stmt.where(UserAccountModel.deleted_at.is_(None))

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

        return UserAccountMapper.to_dto(model) if model else None

    async def find_user_accounts(
        self,
        user_id: UserAccountUserID,
        account_id: UserAccountID | None = None,
        name: AccountName | None = None,
        only_active: bool | None = True,
    ) -> list[UserAccountDTO] | None:
        """Find user account always filtering by user_id (for user-scoped queries)"""
        stmt = select(UserAccountModel).where(UserAccountModel.user_id == user_id.value)
        if only_active:
            stmt = stmt.where(UserAccountModel.deleted_at.is_(None))

        if account_id is not None:
            stmt = stmt.where(UserAccountModel.id == account_id.value)
        else:
            if name is not None:
                stmt = stmt.where(UserAccountModel.name.like(f"%{name.value}%"))

        models = (await self._db.execute(stmt)).scalars()
        return (
            [UserAccountMapper.to_dto_or_fail(model) for model in models]
            if models
            else []
        )

    async def find_user_account_by_id(
        self,
        user_id: UserAccountUserID,
        account_id: UserAccountID,
        only_active: bool | None = True,
    ) -> UserAccountDTO | None:
        stmt = select(UserAccountModel).where(
            UserAccountModel.id == account_id.value,
            UserAccountModel.user_id == user_id.value,
        )
        if only_active:
            stmt = stmt.where(UserAccountModel.deleted_at.is_(None))

        model = (await self._db.execute(stmt)).scalar_one_or_none()
        return UserAccountMapper.to_dto(model)

    async def update_account(self, account: UserAccountDTO) -> UserAccountDTO:
        """Update an existing account"""
        if account.account_id is None:
            raise ValueError("Account ID not given")

        stmt = (
            update(UserAccountModel)
            .where(
                UserAccountModel.id == account.account_id.value,
                UserAccountModel.deleted_at.is_(None),
            )
            .values(
                name=account.name.value,
                currency=account.currency.value,
                balance=account.balance.value,
            )
        )

        result = cast(CursorResult[Any], await self._db.execute(stmt))
        if result.rowcount == 0:
            raise UserAccountNotFoundError(
                f"Account with ID {account.account_id.value} not found or already deleted"
            )

        await self._db.commit()

        return account

    async def delete_account(
        self, account_id: UserAccountID, user_id: UserAccountUserID
    ) -> bool:
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
                UserAccountModel.deleted_at.is_(None),
            )
            .values(deleted_at=UserAccountDeletedAt.now().value)
        )

        result = cast(CursorResult[Any], await self._db.execute(stmt))
        await self._db.commit()

        return result.rowcount > 0
