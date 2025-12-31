from dataclasses import dataclass

from app.context.entry.domain.value_objects import (
    EntryAccountID,
    EntryAmount,
    EntryCategoryID,
    EntryDate,
    EntryDescription,
    EntryHouseholdID,
    EntryID,
    EntryType,
    EntryUserID,
)


@dataclass(frozen=True)
class EntryDTO:
    """Domain DTO for entry entity"""

    user_id: EntryUserID
    account_id: EntryAccountID
    category_id: EntryCategoryID
    entry_type: EntryType
    entry_date: EntryDate
    amount: EntryAmount
    description: EntryDescription
    entry_id: EntryID | None = None
    household_id: EntryHouseholdID | None = None
