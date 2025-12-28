from app.context.household.domain.contracts import (
    HouseholdRepositoryContract,
    RevokeInviteServiceContract,
)
from app.context.household.domain.exceptions import (
    InviteNotFoundError,
    OnlyOwnerCanRevokeError,
)
from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID


class RevokeInviteService(RevokeInviteServiceContract):
    def __init__(self, household_repo: HouseholdRepositoryContract):
        self._household_repo = household_repo

    async def revoke_invite(
        self,
        revoker_user_id: HouseholdUserID,
        household_id: HouseholdID,
        invitee_user_id: HouseholdUserID,
    ) -> None:
        """Revoke a pending household invite"""

        # Check if revoker is the owner
        household = await self._household_repo.find_household_by_id(household_id)
        if not household or household.owner_user_id.value != revoker_user_id.value:
            raise OnlyOwnerCanRevokeError("Only the household owner can revoke invites")

        # Check if there's a pending invite
        member = await self._household_repo.find_member(household_id, invitee_user_id)

        if not member or not member.is_invited:
            raise InviteNotFoundError("No pending invite found for this user")

        await self._household_repo.revoke_or_remove(household_id, invitee_user_id)
