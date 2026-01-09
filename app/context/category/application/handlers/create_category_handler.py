from app.context.category.application.commands import CreateCategoryCommand
from app.context.category.application.contracts import CreateCategoryHandlerContract
from app.context.category.application.dto import CreateCategoryErrorCode, CreateCategoryResult
from app.context.category.domain.contracts.services import CreateCategoryServiceContract
from app.context.category.domain.exceptions import CategoryMapperError, CategoryNameAlreadyExistError
from app.context.category.domain.value_objects import CategoryColor, CategoryName, CategoryUserID
from app.shared.domain.contracts import LoggerContract


class CreateCategoryHandler(CreateCategoryHandlerContract):
    """Handler for create category command"""

    def __init__(self, service: CreateCategoryServiceContract, logger: LoggerContract):
        self._service = service
        self._logger = logger

    async def handle(self, command: CreateCategoryCommand) -> CreateCategoryResult:
        """Execute the create category command"""

        try:
            category_dto = await self._service.create_category(
                user_id=CategoryUserID(command.user_id),
                name=CategoryName(command.name),
                color=CategoryColor(command.color),
            )

            if category_dto.category_id is None:
                self._logger.error(
                    "Category creation returned None category_id",
                    user_id=command.user_id,
                    name=command.name,
                )
                return CreateCategoryResult(
                    error_code=CreateCategoryErrorCode.UNEXPECTED_ERROR,
                    error_message="Error creating category",
                )

            return CreateCategoryResult(
                category_id=category_dto.category_id.value,
                category_name=category_dto.name.value,
            )
        except CategoryNameAlreadyExistError:
            return CreateCategoryResult(
                error_code=CreateCategoryErrorCode.NAME_ALREADY_EXISTS,
                error_message="Category name already exists",
            )
        except CategoryMapperError:
            return CreateCategoryResult(
                error_code=CreateCategoryErrorCode.MAPPER_ERROR,
                error_message="Error mapping model to dto",
            )
        except Exception as e:
            self._logger.error(
                "Unexpected error during category creation",
                user_id=command.user_id,
                name=command.name,
                error=str(e),
            )
            return CreateCategoryResult(
                error_code=CreateCategoryErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
