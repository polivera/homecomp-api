from abc import ABC, abstractmethod

from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID


class RevokeInviteServiceContract(ABC):
    @abstractmethod
    async def revoke_invite(
        self,
        revoker_user_id: HouseholdUserID,
        household_id: HouseholdID,
        invitee_user_id: HouseholdUserID,
    ) -> None:
        """
        Revoke a pending household invite.
        Only the owner can revoke invites.

        Raises:
            OnlyOwnerCanRevokeError: If revoker is not the household owner
            InviteNotFoundError: If no pending invite exists
        """
        pass
