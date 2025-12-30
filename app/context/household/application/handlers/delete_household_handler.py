from app.context.household.application.commands import DeleteHouseholdCommand
from app.context.household.application.contracts import DeleteHouseholdHandlerContract
from app.context.household.application.dto import DeleteHouseholdErrorCode, DeleteHouseholdResult
from app.context.household.domain.contracts import HouseholdRepositoryContract
from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID
from app.shared.domain.contracts import LoggerContract


class DeleteHouseholdHandler(DeleteHouseholdHandlerContract):
    """Handler for delete household command"""

    def __init__(self, repository: HouseholdRepositoryContract, logger: LoggerContract):
        self._repository = repository
        self._logger = logger

    async def handle(self, command: DeleteHouseholdCommand) -> DeleteHouseholdResult:
        """Execute the delete household command"""

        self._logger.debug(
            "Handling delete household command",
            household_id=command.household_id,
            user_id=command.user_id,
        )

        try:
            # Convert primitives to value objects
            success = await self._repository.delete_household(
                household_id=HouseholdID(command.household_id),
                user_id=HouseholdUserID(command.user_id),
            )

            if not success:
                self._logger.debug(
                    "Household not found or user not owner",
                    household_id=command.household_id,
                    user_id=command.user_id,
                )
                return DeleteHouseholdResult(
                    error_code=DeleteHouseholdErrorCode.NOT_FOUND,
                    error_message="Household not found or you are not the owner",
                )

            return DeleteHouseholdResult(success=True)

        except Exception as e:
            self._logger.error("Unexpected error deleting household", household_id=command.household_id, error=str(e))
            return DeleteHouseholdResult(
                error_code=DeleteHouseholdErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
