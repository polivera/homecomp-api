from dataclasses import dataclass


@dataclass(frozen=True)
class UpdateCategoryCommand:
    """Command to update an existing category"""

    user_id: int
    category_id: int
    name: str
    color: str
