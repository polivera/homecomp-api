from app.context.household.application.commands import AcceptInviteCommand
from app.context.household.application.contracts import AcceptInviteHandlerContract
from app.context.household.application.dto import (
    AcceptInviteErrorCode,
    AcceptInviteResult,
)
from app.context.household.domain.contracts import AcceptInviteServiceContract
from app.context.household.domain.exceptions import (
    HouseholdMapperError,
    NotInvitedError,
)
from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID


class AcceptInviteHandler(AcceptInviteHandlerContract):
    """Handler for accept invite command"""

    def __init__(self, service: AcceptInviteServiceContract):
        self._service = service

    async def handle(self, command: AcceptInviteCommand) -> AcceptInviteResult:
        """Execute the accept invite command"""

        try:
            member_dto = await self._service.accept_invite(
                user_id=HouseholdUserID(command.user_id),
                household_id=HouseholdID(command.household_id),
            )

            if member_dto.member_id is None:
                return AcceptInviteResult(
                    error_code=AcceptInviteErrorCode.UNEXPECTED_ERROR,
                    error_message="Error accepting invitation",
                )

            return AcceptInviteResult(
                member_id=member_dto.member_id.value,
                household_id=member_dto.household_id.value,
                user_id=member_dto.user_id.value,
                role=member_dto.role.value,
            )

        except NotInvitedError:
            return AcceptInviteResult(
                error_code=AcceptInviteErrorCode.NOT_INVITED,
                error_message="No pending invite found for this household",
            )
        except HouseholdMapperError:
            return AcceptInviteResult(
                error_code=AcceptInviteErrorCode.MAPPER_ERROR,
                error_message="Error mapping model to DTO",
            )
        except Exception:
            return AcceptInviteResult(
                error_code=AcceptInviteErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
