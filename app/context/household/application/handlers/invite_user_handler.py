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


class InviteUserHandler(InviteUserHandlerContract):
    """Handler for invite user command"""

    def __init__(self, service: InviteUserServiceContract):
        self._service = service

    async def handle(self, command: InviteUserCommand) -> InviteUserResult:
        """Execute the invite user command"""

        try:
            member_dto = await self._service.invite_user(
                inviter_user_id=HouseholdUserID(command.inviter_user_id),
                household_id=HouseholdID(command.household_id),
                invitee_user_id=HouseholdUserID(command.invitee_user_id),
                role=HouseholdRole(command.role),
            )

            if member_dto.member_id is None:
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
            return InviteUserResult(
                error_code=InviteUserErrorCode.ONLY_OWNER_CAN_INVITE,
                error_message="Only the household owner can invite users",
            )
        except AlreadyActiveMemberError:
            return InviteUserResult(
                error_code=InviteUserErrorCode.ALREADY_ACTIVE_MEMBER,
                error_message="User is already an active member of this household",
            )
        except AlreadyInvitedError:
            return InviteUserResult(
                error_code=InviteUserErrorCode.ALREADY_INVITED,
                error_message="User already has a pending invite to this household",
            )
        except HouseholdMapperError:
            return InviteUserResult(
                error_code=InviteUserErrorCode.MAPPER_ERROR,
                error_message="Error mapping model to DTO",
            )
        except Exception:
            return InviteUserResult(
                error_code=InviteUserErrorCode.UNEXPECTED_ERROR,
                error_message="Unexpected error",
            )
