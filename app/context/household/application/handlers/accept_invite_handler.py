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
from app.shared.domain.contracts import LoggerContract


class AcceptInviteHandler(AcceptInviteHandlerContract):
    """Handler for accept invite command"""

    def __init__(self, service: AcceptInviteServiceContract, logger: LoggerContract):
        self._service = service
        self._logger = logger

    async def handle(self, command: AcceptInviteCommand) -> AcceptInviteResult:
        """Execute the accept invite command"""

        self._logger.debug("Handling accept invite command", user_id=command.user_id, household_id=command.household_id)

        try:
            member_dto = await self._service.accept_invite(
                user_id=HouseholdUserID(command.user_id),
                household_id=HouseholdID(command.household_id),
            )

            if member_dto.member_id is None:
                self._logger.error(
                    "Member ID is None after accepting invite",
                    user_id=command.user_id,
                    household_id=command.household_id,
                )
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
            self._logger.debug("No pending invite found", user_id=command.user_id, household_id=command.household_id)
            return AcceptInviteResult(
                error_code=AcceptInviteErrorCode.NOT_INVITED,
                error_message="No pending invite found for this household",
            )
        except HouseholdMapperError:
            self._logger.error("Mapper error accepting invite", household_id=command.household_id)
            return AcceptInviteResult(
                error_code=AcceptInviteErrorCode.MAPPER_ERROR,
                error_message="Error mapping model to DTO",
            )
        except Exception as e:
            self._logger.error("Unexpected error accepting invite", household_id=command.household_id, error=str(e))
            return AcceptInviteResult(
                error_code=AcceptInviteErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
