from app.context.category.domain.contracts.infrastructure import CategoryRepositoryContract
from app.context.category.domain.contracts.services import FindCategoryByIdServiceContract
from app.context.category.domain.dto import CategoryDTO
from app.context.category.domain.value_objects import CategoryID, CategoryUserID
from app.shared.domain.contracts import LoggerContract


class FindCategoryByIdService(FindCategoryByIdServiceContract):
    """Service for finding a category by ID"""

    def __init__(self, category_repository: CategoryRepositoryContract, logger: LoggerContract):
        self._category_repository = category_repository
        self._logger = logger

    async def find_category_by_id(
        self,
        user_id: CategoryUserID,
        category_id: CategoryID,
    ) -> CategoryDTO | None:
        """Find a specific category by ID for a user"""

        self._logger.debug(
            "Finding category by ID", user_id=user_id.value, category_id=category_id.value
        )

        return await self._category_repository.find_user_category_by_id(
            user_id=user_id, category_id=category_id, only_active=True
        )
