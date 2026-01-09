from abc import ABC, abstractmethod

from app.context.category.domain.dto import CategoryDTO
from app.context.category.domain.value_objects import CategoryID, CategoryName, CategoryUserID


class CategoryRepositoryContract(ABC):
    """Contract for category repository operations"""

    @abstractmethod
    async def save_category(self, category: CategoryDTO) -> CategoryDTO:
        """
        Create a new category

        Args:
            category: The category DTO to save

        Returns:
            CategoryDTO of the created category

        Raises:
            CategoryMapperError if cannot map model to dto
            CategoryNameAlreadyExistError if category name already exist for this user
        """
        pass

    @abstractmethod
    async def find_category(
        self,
        category_id: CategoryID | None = None,
        user_id: CategoryUserID | None = None,
        name: CategoryName | None = None,
    ) -> CategoryDTO | None:
        """
        Find a category by ID or by user_id and name

        Args:
            category_id: Category ID to search for
            user_id: User ID to search for (combined with name)
            name: Category name to search for (combined with user_id)

        Returns:
            CategoryDTO if found, None otherwise
        """
        pass

    @abstractmethod
    async def find_user_categories(
        self,
        user_id: CategoryUserID,
        category_id: CategoryID | None = None,
        name: CategoryName | None = None,
        only_active: bool | None = True,
    ) -> list[CategoryDTO] | None:
        """
        Find user categories always filtering by user_id (for user-scoped queries)

        Args:
            user_id: User ID to filter categories for
            category_id: Optional category ID to find specific category
            name: Optional category name for partial match search
            only_active: Whether to exclude soft-deleted categories (default: True)

        Returns:
            List of CategoryDTO if found, None otherwise
        """
        pass

    @abstractmethod
    async def find_user_category_by_id(
        self,
        user_id: CategoryUserID,
        category_id: CategoryID,
        only_active: bool | None = True,
    ) -> CategoryDTO | None:
        """
        Find a specific category by ID for a user

        Args:
            user_id: User ID for authorization
            category_id: Category ID to find
            only_active: Whether to exclude soft-deleted categories (default: True)

        Returns:
            CategoryDTO if found, None otherwise
        """
        pass

    @abstractmethod
    async def update_category(self, category: CategoryDTO) -> CategoryDTO:
        """
        Update an existing category

        Args:
            category: The category DTO with updated values

        Returns:
            Updated CategoryDTO

        Raises:
            CategoryNotFoundError if category not found or already deleted
        """
        pass

    @abstractmethod
    async def delete_category(self, category_id: CategoryID, user_id: CategoryUserID) -> bool:
        """
        Soft delete a category. Returns True if deleted, False if not found/unauthorized

        Args:
            category_id: Category ID to delete
            user_id: User ID (for authorization check)

        Returns:
            True if successfully deleted, False if not found or unauthorized
        """
        pass
