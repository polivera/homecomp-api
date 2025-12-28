from app.context.household.domain.contracts import (
    HouseholdRepositoryContract,
    RemoveMemberServiceContract,
)
from app.context.household.domain.exceptions import (
    CannotRemoveSelfError,
    InviteNotFoundError,
    OnlyOwnerCanRemoveMemberError,
)
from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID


class RemoveMemberService(RemoveMemberServiceContract):
    def __init__(self, household_repo: HouseholdRepositoryContract):
        self._household_repo = household_repo

    async def remove_member(
        self,
        remover_user_id: HouseholdUserID,
        household_id: HouseholdID,
        member_user_id: HouseholdUserID,
    ) -> None:
        """Remove an active member from a household"""

        # Check if remover is the owner
        household = await self._household_repo.find_household_by_id(household_id)
        if not household or household.owner_user_id.value != remover_user_id.value:
            raise OnlyOwnerCanRemoveMemberError(
                "Only the household owner can remove members"
            )

        # Owner cannot remove themselves
        if remover_user_id.value == member_user_id.value:
            raise CannotRemoveSelfError(
                "Owner cannot remove themselves from the household"
            )

        # Check if member exists and is active
        member = await self._household_repo.find_member(household_id, member_user_id)

        if not member or not member.is_active:
            raise InviteNotFoundError(
                "No active member found with this user ID"
            )

        # Remove the member (sets left_at)
        await self._household_repo.revoke_or_remove(household_id, member_user_id)
