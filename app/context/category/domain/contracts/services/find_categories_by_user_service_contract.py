from abc import ABC, abstractmethod

from app.context.category.domain.dto import CategoryDTO
from app.context.category.domain.value_objects import CategoryUserID


class FindCategoriesByUserServiceContract(ABC):
    """Contract for find categories by user service"""

    @abstractmethod
    async def find_categories_by_user(
        self,
        user_id: CategoryUserID,
    ) -> list[CategoryDTO]:
        """
        Find all categories for a user

        Args:
            user_id: ID of the user

        Returns:
            List of CategoryDTO (empty list if none found)
        """
        pass
