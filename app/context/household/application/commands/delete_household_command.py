from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteHouseholdCommand:
    """Command to delete household (soft delete)"""

    household_id: int
    user_id: int
