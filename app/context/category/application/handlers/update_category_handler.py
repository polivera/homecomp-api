from app.context.category.application.commands import UpdateCategoryCommand
from app.context.category.application.contracts import UpdateCategoryHandlerContract
from app.context.category.application.dto import UpdateCategoryErrorCode, UpdateCategoryResult
from app.context.category.domain.contracts.services import UpdateCategoryServiceContract
from app.context.category.domain.exceptions import (
    CategoryMapperError,
    CategoryNameAlreadyExistError,
    CategoryNotFoundError,
)
from app.context.category.domain.value_objects import CategoryColor, CategoryID, CategoryName, CategoryUserID
from app.shared.domain.contracts import LoggerContract


class UpdateCategoryHandler(UpdateCategoryHandlerContract):
    """Handler for update category command"""

    def __init__(self, service: UpdateCategoryServiceContract, logger: LoggerContract):
        self._service = service
        self._logger = logger

    async def handle(self, command: UpdateCategoryCommand) -> UpdateCategoryResult:
        """Execute the update category command"""

        try:
            category_dto = await self._service.update_category(
                user_id=CategoryUserID(command.user_id),
                category_id=CategoryID(command.category_id),
                name=CategoryName(command.name),
                color=CategoryColor(command.color),
            )

            if category_dto.category_id is None:
                self._logger.error(
                    "Category update returned None category_id",
                    user_id=command.user_id,
                    category_id=command.category_id,
                )
                return UpdateCategoryResult(
                    error_code=UpdateCategoryErrorCode.UNEXPECTED_ERROR,
                    error_message="Error updating category",
                )

            return UpdateCategoryResult(
                category_id=category_dto.category_id.value,
                category_name=category_dto.name.value,
            )
        except CategoryNotFoundError:
            return UpdateCategoryResult(
                error_code=UpdateCategoryErrorCode.NOT_FOUND,
                error_message="Category not found",
            )
        except CategoryNameAlreadyExistError:
            return UpdateCategoryResult(
                error_code=UpdateCategoryErrorCode.NAME_ALREADY_EXISTS,
                error_message="Category name already exists",
            )
        except CategoryMapperError:
            return UpdateCategoryResult(
                error_code=UpdateCategoryErrorCode.MAPPER_ERROR,
                error_message="Error mapping model to dto",
            )
        except Exception as e:
            self._logger.error(
                "Unexpected error during category update",
                user_id=command.user_id,
                category_id=command.category_id,
                error=str(e),
            )
            return UpdateCategoryResult(
                error_code=UpdateCategoryErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
