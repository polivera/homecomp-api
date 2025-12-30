from app.context.household.application.commands import CreateHouseholdCommand
from app.context.household.application.contracts import CreateHouseholdHandlerContract
from app.context.household.application.dto import (
    CreateHouseholdErrorCode,
    CreateHouseholdResult,
)
from app.context.household.domain.contracts import CreateHouseholdServiceContract
from app.context.household.domain.exceptions import (
    HouseholdMapperError,
    HouseholdNameAlreadyExistError,
)
from app.context.household.domain.value_objects import HouseholdName, HouseholdUserID
from app.shared.domain.contracts import LoggerContract


class CreateHouseholdHandler(CreateHouseholdHandlerContract):
    """Handler for create household command"""

    def __init__(self, service: CreateHouseholdServiceContract, logger: LoggerContract):
        self._service = service
        self._logger = logger

    async def handle(self, command: CreateHouseholdCommand) -> CreateHouseholdResult:
        """Execute the create household command"""

        self._logger.debug("Handling create household command", user_id=command.user_id, name=command.name)

        try:
            household_dto = await self._service.create_household(
                name=HouseholdName(command.name),
                creator_user_id=HouseholdUserID(command.user_id),
            )

            if household_dto.household_id is None:
                self._logger.error("Household ID is None after creation", user_id=command.user_id)
                return CreateHouseholdResult(
                    error_code=CreateHouseholdErrorCode.UNEXPECTED_ERROR,
                    error_message="Error creating household",
                )

            return CreateHouseholdResult(
                household_id=household_dto.household_id.value,
                household_name=household_dto.name.value,
            )

        except HouseholdNameAlreadyExistError:
            self._logger.debug("Household name already exists", user_id=command.user_id, name=command.name)
            return CreateHouseholdResult(
                error_code=CreateHouseholdErrorCode.NAME_ALREADY_EXISTS,
                error_message="Household name already exists",
            )
        except HouseholdMapperError:
            self._logger.error("Mapper error creating household", user_id=command.user_id)
            return CreateHouseholdResult(
                error_code=CreateHouseholdErrorCode.MAPPER_ERROR,
                error_message="Error mapping model to DTO",
            )
        except Exception as e:
            self._logger.error("Unexpected error creating household", user_id=command.user_id, error=str(e))
            return CreateHouseholdResult(
                error_code=CreateHouseholdErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
