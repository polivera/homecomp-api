from abc import ABC, abstractmethod

from app.context.entry.domain.dto import EntryDTO
from app.context.entry.domain.value_objects import (
    EntryAccountID,
    EntryAmount,
    EntryCategoryID,
    EntryDate,
    EntryDescription,
    EntryHouseholdID,
    EntryType,
    EntryUserID,
)


class CreateEntryServiceContract(ABC):
    """Contract for create entry service"""

    @abstractmethod
    async def create_entry(
        self,
        user_id: EntryUserID,
        account_id: EntryAccountID,
        category_id: EntryCategoryID,
        entry_type: EntryType,
        entry_date: EntryDate,
        amount: EntryAmount,
        description: EntryDescription,
        household_id: EntryHouseholdID | None = None,
    ) -> EntryDTO:
        """
        Create a new entry with validation

        Args:
            user_id: User identifier
            account_id: Account identifier
            category_id: Category identifier
            entry_type: Type of entry (income/expense)
            entry_date: Date of entry
            amount: Amount (non-negative)
            description: Entry description
            household_id: Optional household identifier

        Returns:
            Created entry DTO

        Raises:
            EntryAccountNotBelongsToUserError: If account doesn't belong to user
            EntryCategoryNotFoundError: If category doesn't exist
            EntryCategoryNotBelongsToUserError: If category doesn't belong to user
            EntryMapperError: If mapping fails
        """
        pass
