from app.context.household.application.commands import InviteUserCommand
from app.context.household.application.contracts import InviteUserHandlerContract
from app.context.household.application.dto import InviteUserErrorCode, InviteUserResult
from app.context.household.domain.contracts import InviteUserServiceContract
from app.context.household.domain.exceptions import (
    AlreadyActiveMemberError,
    AlreadyInvitedError,
    HouseholdMapperError,
    OnlyOwnerCanInviteError,
)
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdRole,
    HouseholdUserID,
)
from app.shared.domain.contracts import LoggerContract


class InviteUserHandler(InviteUserHandlerContract):
    """Handler for invite user command"""

    def __init__(self, service: InviteUserServiceContract, logger: LoggerContract):
        self._service = service
        self._logger = logger

    async def handle(self, command: InviteUserCommand) -> InviteUserResult:
        """Execute the invite user command"""

        self._logger.debug(
            "Handling invite user command",
            inviter_user_id=command.inviter_user_id,
            household_id=command.household_id,
            invitee_user_id=command.invitee_user_id,
        )

        try:
            member_dto = await self._service.invite_user(
                inviter_user_id=HouseholdUserID(command.inviter_user_id),
                household_id=HouseholdID(command.household_id),
                invitee_user_id=HouseholdUserID(command.invitee_user_id),
                role=HouseholdRole(command.role),
            )

            if member_dto.member_id is None:
                self._logger.error(
                    "Member ID is None after invitation",
                    household_id=command.household_id,
                    invitee_user_id=command.invitee_user_id,
                )
                return InviteUserResult(
                    error_code=InviteUserErrorCode.UNEXPECTED_ERROR,
                    error_message="Error creating invitation",
                )

            return InviteUserResult(
                member_id=member_dto.member_id.value,
                household_id=member_dto.household_id.value,
                user_id=member_dto.user_id.value,
                role=member_dto.role.value,
            )

        except OnlyOwnerCanInviteError:
            self._logger.debug(
                "Non-owner attempted invite",
                inviter_user_id=command.inviter_user_id,
                household_id=command.household_id,
            )
            return InviteUserResult(
                error_code=InviteUserErrorCode.ONLY_OWNER_CAN_INVITE,
                error_message="Only the household owner can invite users",
            )
        except AlreadyActiveMemberError:
            self._logger.debug(
                "User already active member",
                household_id=command.household_id,
                invitee_user_id=command.invitee_user_id,
            )
            return InviteUserResult(
                error_code=InviteUserErrorCode.ALREADY_ACTIVE_MEMBER,
                error_message="User is already an active member of this household",
            )
        except AlreadyInvitedError:
            self._logger.debug(
                "User already invited",
                household_id=command.household_id,
                invitee_user_id=command.invitee_user_id,
            )
            return InviteUserResult(
                error_code=InviteUserErrorCode.ALREADY_INVITED,
                error_message="User already has a pending invite to this household",
            )
        except HouseholdMapperError:
            self._logger.error("Mapper error inviting user", household_id=command.household_id)
            return InviteUserResult(
                error_code=InviteUserErrorCode.MAPPER_ERROR,
                error_message="Error mapping model to DTO",
            )
        except Exception as e:
            self._logger.error("Unexpected error inviting user", household_id=command.household_id, error=str(e))
            return InviteUserResult(
                error_code=InviteUserErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
