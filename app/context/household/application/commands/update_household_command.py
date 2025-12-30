from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateHouseholdCommand:
    """Command to update household"""

    household_id: int
    user_id: int
    name: str
