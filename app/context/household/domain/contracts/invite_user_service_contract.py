from abc import ABC, abstractmethod

from app.context.household.domain.dto import HouseholdMemberDTO
from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdRole,
    HouseholdUserID,
)


class InviteUserServiceContract(ABC):
    @abstractmethod
    async def invite_user(
        self,
        inviter_user_id: HouseholdUserID,
        household_id: HouseholdID,
        invitee_user_id: HouseholdUserID,
        role: HouseholdRole,
    ) -> HouseholdMemberDTO:
        """
        Invite a user to a household.
        Only the owner can invite users.

        Args:
            inviter_user_id: The user ID of the person sending the invite
            household_id: The household ID to invite the user to
            invitee_user_id: The user ID of the person being invited
            role: The role to assign to the invited user

        Raises:
            OnlyOwnerCanInviteError: If inviter is not the household owner
            AlreadyActiveMemberError: If user is already an active member
            AlreadyInvitedError: If user already has a pending invite
        """
        pass
