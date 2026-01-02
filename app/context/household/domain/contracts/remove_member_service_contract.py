from abc import ABC, abstractmethod

from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID


class RemoveMemberServiceContract(ABC):
    @abstractmethod
    async def remove_member(
        self,
        remover_user_id: HouseholdUserID,
        household_id: HouseholdID,
        member_user_id: HouseholdUserID,
    ) -> None:
        """
        Remove an active member from a household.
        Only the owner can remove members.
        Owner cannot remove themselves.

        Raises:
            OnlyOwnerCanRemoveMemberError: If remover is not the household owner
            CannotRemoveSelfError: If owner tries to remove themselves
            InviteNotFoundError: If member is not found or not active
        """
        pass
