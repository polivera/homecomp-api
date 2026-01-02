from dataclasses import dataclass

from app.shared.domain.value_objects.shared_household_id import SharedHouseholdID


@dataclass(frozen=True)
class EntryHouseholdID(SharedHouseholdID):
    """Entry context-specific wrapper for household identifier"""

    pass
