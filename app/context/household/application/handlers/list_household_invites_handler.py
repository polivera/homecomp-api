from app.context.household.application.contracts import (
    ListHouseholdInvitesHandlerContract,
)
from app.context.household.application.dto import HouseholdMemberResponseDTO
from app.context.household.application.queries import ListHouseholdInvitesQuery
from app.context.household.domain.contracts import HouseholdRepositoryContract
from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID


class ListHouseholdInvitesHandler(ListHouseholdInvitesHandlerContract):
    """Handler for list household invites query"""

    def __init__(self, repository: HouseholdRepositoryContract):
        self._repository = repository

    async def handle(self, query: ListHouseholdInvitesQuery) -> list[HouseholdMemberResponseDTO]:
        """Execute the list household invites query"""

        members = await self._repository.list_household_pending_invites(
            household_id=HouseholdID(query.household_id),
            owner_id=HouseholdUserID(query.user_id),
        )

        return [HouseholdMemberResponseDTO.from_domain_dto(member) for member in members] if members else []
