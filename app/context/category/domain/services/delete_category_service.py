from app.context.category.domain.contracts.infrastructure import CategoryRepositoryContract
from app.context.category.domain.contracts.services import DeleteCategoryServiceContract
from app.context.category.domain.value_objects import CategoryID, CategoryUserID
from app.shared.domain.contracts import LoggerContract


class DeleteCategoryService(DeleteCategoryServiceContract):
    """Service for deleting categories"""

    def __init__(self, category_repository: CategoryRepositoryContract, logger: LoggerContract):
        self._category_repository = category_repository
        self._logger = logger

    async def delete_category(
        self,
        user_id: CategoryUserID,
        category_id: CategoryID,
    ) -> bool:
        """Soft delete a category"""

        self._logger.debug(
            "Deleting category", user_id=user_id.value, category_id=category_id.value
        )

        # Delete and return result
        return await self._category_repository.delete_category(
            category_id=category_id, user_id=user_id
        )
