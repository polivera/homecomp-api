from app.context.household.domain.contracts import (
    AcceptInviteServiceContract,
    HouseholdRepositoryContract,
)
from app.context.household.domain.dto import HouseholdMemberDTO
from app.context.household.domain.exceptions import NotInvitedError
from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID
from app.shared.domain.contracts import LoggerContract


class AcceptInviteService(AcceptInviteServiceContract):
    def __init__(self, household_repo: HouseholdRepositoryContract, logger: LoggerContract):
        self._household_repo = household_repo
        self._logger = logger

    async def accept_invite(
        self,
        user_id: HouseholdUserID,
        household_id: HouseholdID,
    ) -> HouseholdMemberDTO:
        """Accept a pending household invite"""

        self._logger.debug("Accepting household invite", user_id=user_id.value, household_id=household_id.value)

        # Check if user has a pending invite
        member = await self._household_repo.find_member(household_id, user_id)

        if not member or not member.is_invited:
            self._logger.debug("No pending invite found", user_id=user_id.value, household_id=household_id.value)
            raise NotInvitedError("No pending invite found for this household")

        # Accept the invite (sets joined_at)
        return await self._household_repo.accept_invite(household_id, user_id)
