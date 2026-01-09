from app.context.category.application.contracts import FindCategoryByIdHandlerContract
from app.context.category.application.dto import (
    CategoryResponseDTO,
    FindCategoryByIdErrorCode,
    FindCategoryByIdResult,
)
from app.context.category.application.queries import FindCategoryByIdQuery
from app.context.category.domain.contracts.services import FindCategoryByIdServiceContract
from app.context.category.domain.value_objects import CategoryID, CategoryUserID
from app.shared.domain.contracts import LoggerContract


class FindCategoryByIdHandler(FindCategoryByIdHandlerContract):
    """Handler for find category by ID query"""

    def __init__(self, service: FindCategoryByIdServiceContract, logger: LoggerContract):
        self._service = service
        self._logger = logger

    async def handle(self, query: FindCategoryByIdQuery) -> FindCategoryByIdResult:
        """Execute the find category by ID query"""

        try:
            category_dto = await self._service.find_category_by_id(
                user_id=CategoryUserID(query.user_id),
                category_id=CategoryID(query.category_id),
            )

            if category_dto is None:
                return FindCategoryByIdResult(
                    error_code=FindCategoryByIdErrorCode.NOT_FOUND,
                    error_message="Category not found",
                )

            return FindCategoryByIdResult(
                category=CategoryResponseDTO.from_domain_dto(category_dto)
            )
        except Exception as e:
            self._logger.error(
                "Unexpected error during find category by ID",
                user_id=query.user_id,
                category_id=query.category_id,
                error=str(e),
            )
            return FindCategoryByIdResult(
                error_code=FindCategoryByIdErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
