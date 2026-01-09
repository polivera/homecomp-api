from abc import ABC, abstractmethod

from app.context.category.domain.dto import CategoryDTO
from app.context.category.domain.value_objects import CategoryColor, CategoryName, CategoryUserID


class CreateCategoryServiceContract(ABC):
    """Contract for create category service"""

    @abstractmethod
    async def create_category(
        self,
        user_id: CategoryUserID,
        name: CategoryName,
        color: CategoryColor,
    ) -> CategoryDTO:
        """
        Create a new category

        Args:
            user_id: ID of the user who owns the category
            name: Name of the category
            color: Color for the category (hex code)

        Returns:
            CategoryDTO of the created category

        Raises:
            CategoryMapperError if cannot map model to dto
            CategoryNameAlreadyExistError if category name already exist for this user
        """
        pass
