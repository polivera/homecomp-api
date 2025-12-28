from abc import ABC, abstractmethod

from app.context.household.domain.dto import HouseholdMemberDTO
from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID


class AcceptInviteServiceContract(ABC):
    @abstractmethod
    async def accept_invite(
        self,
        user_id: HouseholdUserID,
        household_id: HouseholdID,
    ) -> HouseholdMemberDTO:
        """
        Accept a pending household invite.

        Raises:
            NotInvitedError: If user has no pending invite for this household
        """
        pass
