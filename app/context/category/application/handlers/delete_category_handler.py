from app.context.category.application.commands import DeleteCategoryCommand
from app.context.category.application.contracts import DeleteCategoryHandlerContract
from app.context.category.application.dto import DeleteCategoryErrorCode, DeleteCategoryResult
from app.context.category.domain.contracts.services import DeleteCategoryServiceContract
from app.context.category.domain.value_objects import CategoryID, CategoryUserID
from app.shared.domain.contracts import LoggerContract


class DeleteCategoryHandler(DeleteCategoryHandlerContract):
    """Handler for delete category command"""

    def __init__(self, service: DeleteCategoryServiceContract, logger: LoggerContract):
        self._service = service
        self._logger = logger

    async def handle(self, command: DeleteCategoryCommand) -> DeleteCategoryResult:
        """Execute the delete category command"""

        try:
            deleted = await self._service.delete_category(
                user_id=CategoryUserID(command.user_id),
                category_id=CategoryID(command.category_id),
            )

            if not deleted:
                return DeleteCategoryResult(
                    error_code=DeleteCategoryErrorCode.NOT_FOUND,
                    error_message="Category not found or already deleted",
                )

            return DeleteCategoryResult(deleted=True)
        except Exception as e:
            self._logger.error(
                "Unexpected error during category deletion",
                user_id=command.user_id,
                category_id=command.category_id,
                error=str(e),
            )
            return DeleteCategoryResult(
                error_code=DeleteCategoryErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
