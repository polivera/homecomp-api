from dataclasses import dataclass


@dataclass(frozen=True)
class CreateCategoryCommand:
    """Command to create a new category"""

    user_id: int
    name: str
    color: str
