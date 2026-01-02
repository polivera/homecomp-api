from dataclasses import dataclass


@dataclass(frozen=True)
class ListUserHouseholdsQuery:
    """Query to list all households for a user"""

    user_id: int
