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


class CreateHouseholdHandler(CreateHouseholdHandlerContract):
    """Handler for create household command"""

    def __init__(self, service: CreateHouseholdServiceContract):
        self._service = service

    async def handle(self, command: CreateHouseholdCommand) -> CreateHouseholdResult:
        """Execute the create household command"""

        try:
            household_dto = await self._service.create_household(
                name=HouseholdName(command.name),
                creator_user_id=HouseholdUserID(command.user_id),
            )

            if household_dto.household_id is None:
                return CreateHouseholdResult(
                    error_code=CreateHouseholdErrorCode.UNEXPECTED_ERROR,
                    error_message="Error creating household",
                )

            return CreateHouseholdResult(
                household_id=household_dto.household_id.value,
                household_name=household_dto.name.value,
            )

        except HouseholdNameAlreadyExistError:
            return CreateHouseholdResult(
                error_code=CreateHouseholdErrorCode.NAME_ALREADY_EXISTS,
                error_message="Household name already exists",
            )
        except HouseholdMapperError:
            return CreateHouseholdResult(
                error_code=CreateHouseholdErrorCode.MAPPER_ERROR,
                error_message="Error mapping model to DTO",
            )
        except Exception:
            return CreateHouseholdResult(
                error_code=CreateHouseholdErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
