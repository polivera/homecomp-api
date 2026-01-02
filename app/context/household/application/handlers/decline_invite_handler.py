from app.context.household.application.commands import DeclineInviteCommand
from app.context.household.application.contracts import DeclineInviteHandlerContract
from app.context.household.application.dto import (
    DeclineInviteErrorCode,
    DeclineInviteResult,
)
from app.context.household.domain.contracts import DeclineInviteServiceContract
from app.context.household.domain.exceptions import NotInvitedError
from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID
from app.shared.domain.contracts import LoggerContract


class DeclineInviteHandler(DeclineInviteHandlerContract):
    """Handler for decline invite command"""

    def __init__(self, service: DeclineInviteServiceContract, logger: LoggerContract):
        self._service = service
        self._logger = logger

    async def handle(self, command: DeclineInviteCommand) -> DeclineInviteResult:
        """Execute the decline invite command"""

        self._logger.debug(
            "Handling decline invite command", user_id=command.user_id, household_id=command.household_id
        )

        try:
            await self._service.decline_invite(
                user_id=HouseholdUserID(command.user_id),
                household_id=HouseholdID(command.household_id),
            )

            return DeclineInviteResult(success=True)

        except NotInvitedError:
            self._logger.debug("No pending invite found", user_id=command.user_id, household_id=command.household_id)
            return DeclineInviteResult(
                error_code=DeclineInviteErrorCode.NOT_INVITED,
                error_message="No pending invite found for this household",
            )
        except Exception as e:
            self._logger.error("Unexpected error declining invite", household_id=command.household_id, error=str(e))
            return DeclineInviteResult(
                error_code=DeclineInviteErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
