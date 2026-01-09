from dataclasses import dataclass


@dataclass(frozen=True)
class FindCategoriesByUserQuery:
    """Query to find all categories for a user"""

    user_id: int
