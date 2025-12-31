from abc import ABC, abstractmethod

from app.context.entry.domain.dto import EntryDTO
from app.context.entry.domain.value_objects import (
    EntryAccountID,
    EntryCategoryID,
    EntryDate,
    EntryID,
    EntryMonth,
    EntryUserID,
    EntryYear,
)


class EntryRepositoryContract(ABC):
    """Contract for entry repository"""

    @abstractmethod
    async def save_entry(self, entry: EntryDTO) -> EntryDTO:
        """
        Create a new entry

        Args:
            entry: Entry DTO to save

        Returns:
            Saved entry DTO with generated ID

        Raises:
            EntryMapperError: If mapping fails
        """
        pass

    @abstractmethod
    async def find_entry_by_id(
        self,
        entry_id: EntryID,
        user_id: EntryUserID,
    ) -> EntryDTO | None:
        """
        Find entry by ID (with user_id check for security)

        Args:
            entry_id: Entry identifier
            user_id: User identifier (for security check)

        Returns:
            Entry DTO if found and belongs to user, None otherwise
        """
        pass

    @abstractmethod
    async def find_entries_by_account_and_month(
        self,
        user_id: EntryUserID,
        account_id: EntryAccountID,
        month: EntryMonth,
        year: EntryYear,
        last_entry_date: EntryDate | None = None,
    ) -> list[EntryDTO]:
        """
        Find all entries for a specific account in a given month/year

        Args:
            user_id: User identifier (for security check)
            account_id: Account identifier
            month: Month (1-12)
            year: Year (e.g., 2025)

        Returns:
            List of entry DTOs (empty list if none found)
        """
        pass

    @abstractmethod
    async def update_entry(self, entry: EntryDTO) -> EntryDTO:
        """
        Update an existing entry

        Args:
            entry: Entry DTO with updated values (must have entry_id)

        Returns:
            Updated entry DTO

        Raises:
            EntryNotFoundError: If entry doesn't exist
            EntryMapperError: If mapping fails
        """
        pass

    @abstractmethod
    async def delete_entry(
        self,
        entry_id: EntryID,
        user_id: EntryUserID,
    ) -> bool:
        """
        Hard delete an entry

        Args:
            entry_id: Entry identifier
            user_id: User identifier (for security check)

        Returns:
            True if deleted, False if not found or doesn't belong to user
        """
        pass

    @abstractmethod
    async def verify_account_belongs_to_user(
        self,
        account_id: EntryAccountID,
        user_id: EntryUserID,
    ) -> bool:
        """
        Verify that an account belongs to a specific user

        Args:
            account_id: Account identifier
            user_id: User identifier

        Returns:
            True if account belongs to user, False otherwise
        """
        pass

    @abstractmethod
    async def verify_category_belongs_to_user(
        self,
        category_id: EntryCategoryID,
        user_id: EntryUserID,
    ) -> bool:
        """
        Verify that a category belongs to a specific user

        Args:
            category_id: Category identifier
            user_id: User identifier

        Returns:
            True if category belongs to user, False otherwise
        """
        pass
