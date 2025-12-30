from app.context.household.application.commands import DeleteHouseholdCommand
from app.context.household.application.contracts import DeleteHouseholdHandlerContract
from app.context.household.application.dto import DeleteHouseholdErrorCode, DeleteHouseholdResult
from app.context.household.domain.contracts import HouseholdRepositoryContract
from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID


class DeleteHouseholdHandler(DeleteHouseholdHandlerContract):
    """Handler for delete household command"""

    def __init__(self, repository: HouseholdRepositoryContract):
        self._repository = repository

    async def handle(self, command: DeleteHouseholdCommand) -> DeleteHouseholdResult:
        """Execute the delete household command"""

        try:
            # Convert primitives to value objects
            success = await self._repository.delete_household(
                household_id=HouseholdID(command.household_id),
                user_id=HouseholdUserID(command.user_id),
            )

            if not success:
                return DeleteHouseholdResult(
                    error_code=DeleteHouseholdErrorCode.NOT_FOUND,
                    error_message="Household not found or you are not the owner",
                )

            return DeleteHouseholdResult(success=True)

        except Exception:
            return DeleteHouseholdResult(
                error_code=DeleteHouseholdErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
