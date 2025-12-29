from app.context.household.domain.contracts import (
    AcceptInviteServiceContract,
    HouseholdRepositoryContract,
)
from app.context.household.domain.dto import HouseholdMemberDTO
from app.context.household.domain.exceptions import NotInvitedError
from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID


class AcceptInviteService(AcceptInviteServiceContract):
    def __init__(self, household_repo: HouseholdRepositoryContract):
        self._household_repo = household_repo

    async def accept_invite(
        self,
        user_id: HouseholdUserID,
        household_id: HouseholdID,
    ) -> HouseholdMemberDTO:
        """Accept a pending household invite"""

        # Check if user has a pending invite
        member = await self._household_repo.find_member(household_id, user_id)

        if not member or not member.is_invited:
            raise NotInvitedError("No pending invite found for this household")

        # Accept the invite (sets joined_at)
        return await self._household_repo.accept_invite(household_id, user_id)
