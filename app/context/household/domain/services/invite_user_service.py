from datetime import UTC, datetime

from app.context.household.domain.contracts import (
    HouseholdRepositoryContract,
    InviteUserServiceContract,
)
from app.context.household.domain.dto import HouseholdMemberDTO
from app.context.household.domain.exceptions import (
    AlreadyActiveMemberError,
    AlreadyInvitedError,
    OnlyOwnerCanInviteError,
)
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdRole,
    HouseholdUserID,
)
from app.shared.domain.contracts import LoggerContract


class InviteUserService(InviteUserServiceContract):
    def __init__(
        self,
        household_repo: HouseholdRepositoryContract,
        logger: LoggerContract,
    ):
        self._household_repo = household_repo
        self._logger = logger

    async def invite_user(
        self,
        inviter_user_id: HouseholdUserID,
        household_id: HouseholdID,
        invitee_user_id: HouseholdUserID,
        role: HouseholdRole,
    ) -> HouseholdMemberDTO:
        """
        Invite a user to a household.
        """

        self._logger.debug(
            "Inviting user to household",
            inviter_user_id=inviter_user_id.value,
            household_id=household_id.value,
            invitee_user_id=invitee_user_id.value,
            role=role.value,
        )

        household = await self._household_repo.find_household_by_id(household_id)
        if not household or household.owner_user_id.value != inviter_user_id.value:
            self._logger.warning(
                "Non-owner attempted to invite user",
                inviter_user_id=inviter_user_id.value,
                household_id=household_id.value,
            )
            raise OnlyOwnerCanInviteError("Only the household owner can invite users")

        existing_member = await self._household_repo.find_member(household_id, invitee_user_id)

        if existing_member:
            if existing_member.is_active:
                self._logger.debug(
                    "User already active member",
                    household_id=household_id.value,
                    user_id=invitee_user_id.value,
                )
                raise AlreadyActiveMemberError("User is already an active member of this household")
            if existing_member.is_invited:
                self._logger.debug(
                    "User already has pending invite",
                    household_id=household_id.value,
                    user_id=invitee_user_id.value,
                )
                raise AlreadyInvitedError("User already has a pending invite to this household")

        # 3. Create invite (household_member with joined_at=None)
        member_dto = HouseholdMemberDTO(
            member_id=None,
            household_id=household_id,
            user_id=invitee_user_id,
            role=role,
            joined_at=None,  # NULL = invited
            invited_by_user_id=inviter_user_id,
            invited_at=datetime.now(UTC),
        )

        return await self._household_repo.create_member(member_dto)
