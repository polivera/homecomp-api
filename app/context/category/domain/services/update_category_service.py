from app.context.category.domain.contracts.infrastructure import CategoryRepositoryContract
from app.context.category.domain.contracts.services import UpdateCategoryServiceContract
from app.context.category.domain.dto import CategoryDTO
from app.context.category.domain.exceptions import CategoryNotFoundError
from app.context.category.domain.value_objects import CategoryColor, CategoryID, CategoryName, CategoryUserID
from app.shared.domain.contracts import LoggerContract


class UpdateCategoryService(UpdateCategoryServiceContract):
    """Service for updating categories"""

    def __init__(self, category_repository: CategoryRepositoryContract, logger: LoggerContract):
        self._category_repository = category_repository
        self._logger = logger

    async def update_category(
        self,
        user_id: CategoryUserID,
        category_id: CategoryID,
        name: CategoryName,
        color: CategoryColor,
    ) -> CategoryDTO:
        """Update an existing category"""

        self._logger.debug(
            "Updating category",
            user_id=user_id.value,
            category_id=category_id.value,
            name=name.value,
            color=color.value
        )

        # Find existing category
        existing_category = await self._category_repository.find_user_category_by_id(
            user_id=user_id, category_id=category_id, only_active=True
        )

        if not existing_category:
            raise CategoryNotFoundError(f"Category {category_id.value} not found for user {user_id.value}")

        # Create updated DTO
        updated_category = CategoryDTO(
            category_id=category_id,
            user_id=user_id,
            name=name,
            color=color,
            deleted_at=existing_category.deleted_at,
        )

        # Save and return updated category
        return await self._category_repository.update_category(updated_category)
