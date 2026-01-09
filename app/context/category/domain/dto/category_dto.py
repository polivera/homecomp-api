from dataclasses import dataclass

from app.context.category.domain.value_objects import (
    CategoryColor,
    CategoryDeletedAt,
    CategoryID,
    CategoryName,
    CategoryUserID,
)


@dataclass(frozen=True)
class CategoryDTO:
    """Domain DTO for category entity - categories are global and independent"""

    user_id: CategoryUserID
    name: CategoryName
    color: CategoryColor
    category_id: CategoryID | None = None
    deleted_at: CategoryDeletedAt | None = None

    @property
    def is_deleted(self) -> bool:
        """Check if the category is soft deleted"""
        return self.deleted_at is not None
