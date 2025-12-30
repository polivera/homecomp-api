from dataclasses import dataclass


@dataclass(frozen=True)
class HouseholdResponse:
    """Shared response schema for household data"""

    id: int
    name: str
    owner_user_id: int
    created_at: str  # ISO format datetime string
