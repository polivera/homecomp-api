from dataclasses import dataclass


@dataclass(frozen=True)
class FindCategoryByIdQuery:
    """Query to find a category by ID"""

    user_id: int
    category_id: int
