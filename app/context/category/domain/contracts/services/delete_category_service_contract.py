from abc import ABC, abstractmethod

from app.context.category.domain.value_objects import CategoryID, CategoryUserID


class DeleteCategoryServiceContract(ABC):
    """Contract for delete category service"""

    @abstractmethod
    async def delete_category(
        self,
        user_id: CategoryUserID,
        category_id: CategoryID,
    ) -> bool:
        """
        Soft delete a category

        Args:
            user_id: ID of the user who owns the category (for authorization)
            category_id: ID of the category to delete

        Returns:
            True if successfully deleted, False if not found or unauthorized

        Raises:
            CategoryNotFoundError if category not found
        """
        pass
