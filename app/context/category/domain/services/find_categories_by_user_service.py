from app.context.category.domain.contracts.infrastructure import CategoryRepositoryContract
from app.context.category.domain.contracts.services import FindCategoriesByUserServiceContract
from app.context.category.domain.dto import CategoryDTO
from app.context.category.domain.value_objects import CategoryUserID
from app.shared.domain.contracts import LoggerContract


class FindCategoriesByUserService(FindCategoriesByUserServiceContract):
    """Service for finding all categories for a user"""

    def __init__(self, category_repository: CategoryRepositoryContract, logger: LoggerContract):
        self._category_repository = category_repository
        self._logger = logger

    async def find_categories_by_user(
        self,
        user_id: CategoryUserID,
    ) -> list[CategoryDTO]:
        """Find all categories for a user"""

        self._logger.debug("Finding categories by user", user_id=user_id.value)

        categories = await self._category_repository.find_user_categories(
            user_id=user_id, only_active=True
        )

        return categories if categories else []
