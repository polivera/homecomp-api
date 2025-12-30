from app.context.household.application.commands import UpdateHouseholdCommand
from app.context.household.application.contracts import UpdateHouseholdHandlerContract
from app.context.household.application.dto import UpdateHouseholdErrorCode, UpdateHouseholdResult
from app.context.household.domain.contracts import UpdateHouseholdServiceContract
from app.context.household.domain.exceptions import (
    HouseholdMapperError,
    HouseholdNameAlreadyExistError,
    HouseholdNotFoundError,
    OnlyOwnerCanUpdateError,
)
from app.context.household.domain.value_objects import HouseholdID, HouseholdName, HouseholdUserID


class UpdateHouseholdHandler(UpdateHouseholdHandlerContract):
    """Handler for update household command"""

    def __init__(self, service: UpdateHouseholdServiceContract):
        self._service = service

    async def handle(self, command: UpdateHouseholdCommand) -> UpdateHouseholdResult:
        """Execute the update household command"""

        try:
            # Convert primitives to value objects
            updated = await self._service.update_household(
                household_id=HouseholdID(command.household_id),
                user_id=HouseholdUserID(command.user_id),
                name=HouseholdName(command.name),
            )

            if updated.household_id is None:
                return UpdateHouseholdResult(
                    error_code=UpdateHouseholdErrorCode.UNEXPECTED_ERROR,
                    error_message="Error updating household",
                )

            # Return success with primitives
            return UpdateHouseholdResult(
                household_id=updated.household_id.value,
                household_name=updated.name.value,
                owner_user_id=updated.owner_user_id.value,
            )

        except HouseholdNotFoundError:
            return UpdateHouseholdResult(
                error_code=UpdateHouseholdErrorCode.NOT_FOUND,
                error_message="Household not found",
            )
        except OnlyOwnerCanUpdateError:
            return UpdateHouseholdResult(
                error_code=UpdateHouseholdErrorCode.NOT_OWNER,
                error_message="Only the household owner can update the household",
            )
        except HouseholdNameAlreadyExistError:
            return UpdateHouseholdResult(
                error_code=UpdateHouseholdErrorCode.NAME_ALREADY_EXISTS,
                error_message="Household name already exists",
            )
        except HouseholdMapperError:
            return UpdateHouseholdResult(
                error_code=UpdateHouseholdErrorCode.MAPPER_ERROR,
                error_message="Error mapping model to dto",
            )
        except Exception:
            return UpdateHouseholdResult(
                error_code=UpdateHouseholdErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
