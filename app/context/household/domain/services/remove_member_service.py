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
from app.shared.domain.contracts import LoggerContract


class RemoveMemberService(RemoveMemberServiceContract):
    def __init__(self, household_repo: HouseholdRepositoryContract, logger: LoggerContract):
        self._household_repo = household_repo
        self._logger = logger

    async def remove_member(
        self,
        remover_user_id: HouseholdUserID,
        household_id: HouseholdID,
        member_user_id: HouseholdUserID,
    ) -> None:
        """Remove an active member from a household"""

        self._logger.debug(
            "Removing member from household",
            remover_user_id=remover_user_id.value,
            household_id=household_id.value,
            member_user_id=member_user_id.value,
        )

        # Check if remover is the owner
        household = await self._household_repo.find_household_by_id(household_id)
        if not household or household.owner_user_id.value != remover_user_id.value:
            self._logger.warning(
                "Non-owner attempted to remove member",
                remover_user_id=remover_user_id.value,
                household_id=household_id.value,
            )
            raise OnlyOwnerCanRemoveMemberError("Only the household owner can remove members")

        # Owner cannot remove themselves
        if remover_user_id.value == member_user_id.value:
            self._logger.debug("Owner attempted to remove themselves", user_id=remover_user_id.value)
            raise CannotRemoveSelfError("Owner cannot remove themselves from the household")

        # Check if member exists and is active
        member = await self._household_repo.find_member(household_id, member_user_id)

        if not member or not member.is_active:
            self._logger.debug(
                "Member not found or not active",
                household_id=household_id.value,
                member_user_id=member_user_id.value,
            )
            raise InviteNotFoundError("No active member found with this user ID")

        await self._household_repo.revoke_or_remove(household_id, member_user_id)
