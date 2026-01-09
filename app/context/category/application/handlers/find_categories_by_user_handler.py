from app.context.category.application.contracts import FindCategoriesByUserHandlerContract
from app.context.category.application.dto import (
    CategoryResponseDTO,
    FindCategoriesByUserErrorCode,
    FindCategoriesByUserResult,
)
from app.context.category.application.queries import FindCategoriesByUserQuery
from app.context.category.domain.contracts.services import FindCategoriesByUserServiceContract
from app.context.category.domain.value_objects import CategoryUserID
from app.shared.domain.contracts import LoggerContract


class FindCategoriesByUserHandler(FindCategoriesByUserHandlerContract):
    """Handler for find categories by user query"""

    def __init__(self, service: FindCategoriesByUserServiceContract, logger: LoggerContract):
        self._service = service
        self._logger = logger

    async def handle(self, query: FindCategoriesByUserQuery) -> FindCategoriesByUserResult:
        """Execute the find categories by user query"""

        try:
            categories = await self._service.find_categories_by_user(
                user_id=CategoryUserID(query.user_id),
            )

            # Convert domain DTOs to response DTOs
            response_categories = [
                CategoryResponseDTO.from_domain_dto(category) for category in categories
            ]

            return FindCategoriesByUserResult(categories=response_categories)
        except Exception as e:
            self._logger.error(
                "Unexpected error during find categories by user",
                user_id=query.user_id,
                error=str(e),
            )
            return FindCategoriesByUserResult(
                error_code=FindCategoriesByUserErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
