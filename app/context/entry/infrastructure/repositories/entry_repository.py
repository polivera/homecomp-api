from sqlalchemy import delete, extract, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.entry.domain.contracts.infrastructure import EntryRepositoryContract
from app.context.entry.domain.dto import EntryDTO
from app.context.entry.domain.exceptions import EntryNotFoundError
from app.context.entry.domain.value_objects import (
    EntryAccountID,
    EntryCategoryID,
    EntryID,
    EntryUserID,
)
from app.context.entry.infrastructure.mappers import EntryMapper
from app.context.entry.infrastructure.models import EntryModel
from app.context.user_account.infrastructure.models.user_account_model import (
    UserAccountModel,
)


class EntryRepository(EntryRepositoryContract):
    """Repository for entry entity"""

    def __init__(self, db: AsyncSession):
        self._db = db

    async def save_entry(self, entry: EntryDTO) -> EntryDTO:
        """Create a new entry"""
        model = EntryMapper.to_model(entry)
        self._db.add(model)
        await self._db.commit()
        await self._db.refresh(model)
        return EntryMapper.to_dto_or_fail(model)

    async def find_entry_by_id(
        self,
        entry_id: EntryID,
        user_id: EntryUserID,
    ) -> EntryDTO | None:
        """Find entry by ID with user security check"""
        stmt = select(EntryModel).where(
            EntryModel.id == entry_id.value,
            EntryModel.user_id == user_id.value,
        )
        result = await self._db.execute(stmt)
        model = result.scalar_one_or_none()
        return EntryMapper.to_dto(model)

    async def find_entries_by_account_and_month(
        self,
        user_id: EntryUserID,
        account_id: EntryAccountID,
        month: int,
        year: int,
    ) -> list[EntryDTO]:
        """Find all entries for account in specific month/year"""
        stmt = (
            select(EntryModel)
            .where(
                EntryModel.user_id == user_id.value,
                EntryModel.account_id == account_id.value,
                extract("month", EntryModel.entry_date) == month,
                extract("year", EntryModel.entry_date) == year,
            )
            .order_by(EntryModel.entry_date.desc())
        )
        result = await self._db.execute(stmt)
        models = result.scalars().all()
        return [EntryMapper.to_dto_or_fail(model) for model in models]

    async def update_entry(self, entry: EntryDTO) -> EntryDTO:
        """Update an existing entry"""
        if entry.entry_id is None:
            raise ValueError("Entry ID is required for update")

        # Get existing entry
        existing = await self.find_entry_by_id(entry.entry_id, entry.user_id)
        if not existing:
            raise EntryNotFoundError(f"Entry with ID {entry.entry_id.value} not found")

        # Convert DTO to model and update
        model = EntryMapper.to_model(entry)
        await self._db.merge(model)
        await self._db.commit()

        # Re-fetch to get updated values
        updated = await self.find_entry_by_id(entry.entry_id, entry.user_id)
        if not updated:
            raise EntryNotFoundError(f"Entry with ID {entry.entry_id.value} not found after update")

        return updated

    async def delete_entry(
        self,
        entry_id: EntryID,
        user_id: EntryUserID,
    ) -> bool:
        """Hard delete an entry"""
        stmt = delete(EntryModel).where(
            EntryModel.id == entry_id.value,
            EntryModel.user_id == user_id.value,
        )
        result = await self._db.execute(stmt)
        await self._db.commit()
        return result.rowcount > 0

    async def verify_account_belongs_to_user(
        self,
        account_id: EntryAccountID,
        user_id: EntryUserID,
    ) -> bool:
        """Verify account belongs to user"""
        stmt = select(UserAccountModel).where(
            UserAccountModel.id == account_id.value,
            UserAccountModel.user_id == user_id.value,
            UserAccountModel.deleted_at.is_(None),
        )
        result = await self._db.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def verify_category_belongs_to_user(
        self,
        category_id: EntryCategoryID,
        user_id: EntryUserID,
    ) -> bool:
        """Verify category belongs to user"""
        # Import here to avoid circular dependency
        from app.context.category.infrastructure.models.category_model import (
            CategoryModel,
        )

        stmt = select(CategoryModel).where(
            CategoryModel.id == category_id.value,
            CategoryModel.user_id == user_id.value,
            CategoryModel.deleted_at.is_(None),
        )
        result = await self._db.execute(stmt)
        return result.scalar_one_or_none() is not None
