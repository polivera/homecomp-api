from app.context.category.domain.contracts.infrastructure import CategoryRepositoryContract
from app.context.category.domain.contracts.services import CreateCategoryServiceContract
from app.context.category.domain.dto import CategoryDTO
from app.context.category.domain.value_objects import CategoryColor, CategoryName, CategoryUserID
from app.shared.domain.contracts import LoggerContract


class CreateCategoryService(CreateCategoryServiceContract):
    """Service for creating categories"""

    def __init__(self, category_repository: CategoryRepositoryContract, logger: LoggerContract):
        self._category_repository = category_repository
        self._logger = logger

    async def create_category(
        self,
        user_id: CategoryUserID,
        name: CategoryName,
        color: CategoryColor,
    ) -> CategoryDTO:
        """Create a new category with validation"""

        self._logger.debug("Creating category", user_id=user_id.value, name=name.value, color=color.value)

        # Create new category DTO (without ID, will be assigned by database)
        category_dto = CategoryDTO(
            user_id=user_id,
            name=name,
            color=color,
        )

        # Save and return the new category
        return await self._category_repository.save_category(category_dto)
