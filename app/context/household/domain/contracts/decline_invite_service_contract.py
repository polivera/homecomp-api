from abc import ABC, abstractmethod

from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID


class DeclineInviteServiceContract(ABC):
    @abstractmethod
    async def decline_invite(
        self,
        user_id: HouseholdUserID,
        household_id: HouseholdID,
    ) -> None:
        """
        Decline a pending household invite.

        Raises:
            NotInvitedError: If user has no pending invite for this household
        """
        pass
