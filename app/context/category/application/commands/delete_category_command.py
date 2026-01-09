from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteCategoryCommand:
    """Command to delete a category"""

    user_id: int
    category_id: int
