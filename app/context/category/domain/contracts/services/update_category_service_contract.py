from abc import ABC, abstractmethod

from app.context.category.domain.dto import CategoryDTO
from app.context.category.domain.value_objects import CategoryColor, CategoryID, CategoryName, CategoryUserID


class UpdateCategoryServiceContract(ABC):
    """Contract for update category service"""

    @abstractmethod
    async def update_category(
        self,
        user_id: CategoryUserID,
        category_id: CategoryID,
        name: CategoryName,
        color: CategoryColor,
    ) -> CategoryDTO:
        """
        Update an existing category

        Args:
            user_id: ID of the user who owns the category
            category_id: ID of the category to update
            name: New name for the category
            color: New color for the category (hex code)

        Returns:
            CategoryDTO of the updated category

        Raises:
            CategoryNotFoundError if category not found
            CategoryNameAlreadyExistError if new name already exists for this user
        """
        pass
