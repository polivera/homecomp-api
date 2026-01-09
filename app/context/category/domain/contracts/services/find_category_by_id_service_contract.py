from abc import ABC, abstractmethod

from app.context.category.domain.dto import CategoryDTO
from app.context.category.domain.value_objects import CategoryID, CategoryUserID


class FindCategoryByIdServiceContract(ABC):
    """Contract for find category by ID service"""

    @abstractmethod
    async def find_category_by_id(
        self,
        user_id: CategoryUserID,
        category_id: CategoryID,
    ) -> CategoryDTO | None:
        """
        Find a specific category by ID for a user

        Args:
            user_id: ID of the user who owns the category
            category_id: ID of the category to find

        Returns:
            CategoryDTO if found, None otherwise
        """
        pass
