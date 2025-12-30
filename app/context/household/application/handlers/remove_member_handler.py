from app.context.household.application.commands import RemoveMemberCommand
from app.context.household.application.contracts import RemoveMemberHandlerContract
from app.context.household.application.dto import (
    RemoveMemberErrorCode,
    RemoveMemberResult,
)
from app.context.household.domain.contracts import RemoveMemberServiceContract
from app.context.household.domain.exceptions import (
    CannotRemoveSelfError,
    InviteNotFoundError,
    OnlyOwnerCanRemoveMemberError,
)
from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID
from app.shared.domain.contracts import LoggerContract


class RemoveMemberHandler(RemoveMemberHandlerContract):
    """Handler for remove member command"""

    def __init__(self, service: RemoveMemberServiceContract, logger: LoggerContract):
        self._service = service
        self._logger = logger

    async def handle(self, command: RemoveMemberCommand) -> RemoveMemberResult:
        """Execute the remove member command"""

        self._logger.debug(
            "Handling remove member command",
            remover_user_id=command.remover_user_id,
            household_id=command.household_id,
            member_user_id=command.member_user_id,
        )

        try:
            await self._service.remove_member(
                remover_user_id=HouseholdUserID(command.remover_user_id),
                household_id=HouseholdID(command.household_id),
                member_user_id=HouseholdUserID(command.member_user_id),
            )

            return RemoveMemberResult(success=True)

        except OnlyOwnerCanRemoveMemberError:
            self._logger.debug(
                "Non-owner attempted to remove member",
                remover_user_id=command.remover_user_id,
                household_id=command.household_id,
            )
            return RemoveMemberResult(
                error_code=RemoveMemberErrorCode.ONLY_OWNER_CAN_REMOVE,
                error_message="Only the household owner can remove members",
            )
        except CannotRemoveSelfError:
            self._logger.debug("Owner attempted to remove themselves", user_id=command.remover_user_id)
            return RemoveMemberResult(
                error_code=RemoveMemberErrorCode.CANNOT_REMOVE_SELF,
                error_message="Owner cannot remove themselves from the household",
            )
        except InviteNotFoundError:
            self._logger.debug(
                "Member not found",
                household_id=command.household_id,
                member_user_id=command.member_user_id,
            )
            return RemoveMemberResult(
                error_code=RemoveMemberErrorCode.MEMBER_NOT_FOUND,
                error_message="No active member found with this user ID",
            )
        except Exception as e:
            self._logger.error("Unexpected error removing member", household_id=command.household_id, error=str(e))
            return RemoveMemberResult(
                error_code=RemoveMemberErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
