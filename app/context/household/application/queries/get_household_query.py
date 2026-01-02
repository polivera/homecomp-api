from dataclasses import dataclass


@dataclass(frozen=True)
class GetHouseholdQuery:
    """Query to get a household by ID"""

    household_id: int
    user_id: int  # For access check (must be owner or active member)
