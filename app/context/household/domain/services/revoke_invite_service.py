from app.context.household.domain.contracts import (
    HouseholdRepositoryContract,
    RevokeInviteServiceContract,
)
from app.context.household.domain.exceptions import (
    InviteNotFoundError,
    OnlyOwnerCanRevokeError,
)
from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID
from app.shared.domain.contracts import LoggerContract


class RevokeInviteService(RevokeInviteServiceContract):
    def __init__(self, household_repo: HouseholdRepositoryContract, logger: LoggerContract):
        self._household_repo = household_repo
        self._logger = logger

    async def revoke_invite(
        self,
        revoker_user_id: HouseholdUserID,
        household_id: HouseholdID,
        invitee_user_id: HouseholdUserID,
    ) -> None:
        """Revoke a pending household invite"""

        self._logger.debug(
            "Revoking invite",
            revoker_user_id=revoker_user_id.value,
            household_id=household_id.value,
            invitee_user_id=invitee_user_id.value,
        )

        # Check if revoker is the owner
        household = await self._household_repo.find_household_by_id(household_id)
        if not household or household.owner_user_id.value != revoker_user_id.value:
            self._logger.warning(
                "Non-owner attempted to revoke invite",
                revoker_user_id=revoker_user_id.value,
                household_id=household_id.value,
            )
            raise OnlyOwnerCanRevokeError("Only the household owner can revoke invites")

        # Check if there's a pending invite
        member = await self._household_repo.find_member(household_id, invitee_user_id)

        if not member or not member.is_invited:
            self._logger.debug(
                "No pending invite found to revoke",
                household_id=household_id.value,
                invitee_user_id=invitee_user_id.value,
            )
            raise InviteNotFoundError("No pending invite found for this user")

        await self._household_repo.revoke_or_remove(household_id, invitee_user_id)
        self._logger.debug(
            "Invite revoked successfully",
            household_id=household_id.value,
            invitee_user_id=invitee_user_id.value,
        )
