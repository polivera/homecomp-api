from app.context.household.domain.contracts import (
    DeclineInviteServiceContract,
    HouseholdRepositoryContract,
)
from app.context.household.domain.exceptions import NotInvitedError
from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID
from app.shared.domain.contracts import LoggerContract


class DeclineInviteService(DeclineInviteServiceContract):
    def __init__(self, household_repo: HouseholdRepositoryContract, logger: LoggerContract):
        self._household_repo = household_repo
        self._logger = logger

    async def decline_invite(
        self,
        user_id: HouseholdUserID,
        household_id: HouseholdID,
    ) -> None:
        """Decline a pending household invite"""

        self._logger.debug("Declining household invite", user_id=user_id.value, household_id=household_id.value)

        # Check if user has a pending invite
        member = await self._household_repo.find_member(household_id, user_id)

        if not member or not member.is_invited:
            self._logger.debug("No pending invite found", user_id=user_id.value, household_id=household_id.value)
            raise NotInvitedError("No pending invite found for this household")

        await self._household_repo.revoke_or_remove(household_id, user_id)
