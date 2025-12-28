from app.context.household.application.commands import DeclineInviteCommand
from app.context.household.application.contracts import DeclineInviteHandlerContract
from app.context.household.application.dto import (
    DeclineInviteErrorCode,
    DeclineInviteResult,
)
from app.context.household.domain.contracts import DeclineInviteServiceContract
from app.context.household.domain.exceptions import NotInvitedError
from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID


class DeclineInviteHandler(DeclineInviteHandlerContract):
    """Handler for decline invite command"""

    def __init__(self, service: DeclineInviteServiceContract):
        self._service = service

    async def handle(self, command: DeclineInviteCommand) -> DeclineInviteResult:
        """Execute the decline invite command"""

        try:
            await self._service.decline_invite(
                user_id=HouseholdUserID(command.user_id),
                household_id=HouseholdID(command.household_id),
            )

            return DeclineInviteResult(success=True)

        except NotInvitedError:
            return DeclineInviteResult(
                error_code=DeclineInviteErrorCode.NOT_INVITED,
                error_message="No pending invite found for this household",
            )
        except Exception:
            return DeclineInviteResult(
                error_code=DeclineInviteErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
