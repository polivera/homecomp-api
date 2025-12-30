from app.context.household.application.contracts import (
    ListHouseholdInvitesHandlerContract,
)
from app.context.household.application.dto import HouseholdMemberResponseDTO
from app.context.household.application.queries import ListHouseholdInvitesQuery
from app.context.household.domain.contracts import HouseholdRepositoryContract
from app.context.household.domain.value_objects import HouseholdID, HouseholdUserID
from app.shared.domain.contracts import LoggerContract


class ListHouseholdInvitesHandler(ListHouseholdInvitesHandlerContract):
    """Handler for list household invites query"""

    def __init__(self, repository: HouseholdRepositoryContract, logger: LoggerContract):
        self._repository = repository
        self._logger = logger

    async def handle(self, query: ListHouseholdInvitesQuery) -> list[HouseholdMemberResponseDTO]:
        """Execute the list household invites query"""

        self._logger.debug(
            "Handling list household invites query",
            household_id=query.household_id,
            user_id=query.user_id,
        )

        members = await self._repository.list_household_pending_invites(
            household_id=HouseholdID(query.household_id),
            owner_id=HouseholdUserID(query.user_id),
        )

        return [HouseholdMemberResponseDTO.from_domain_dto(member) for member in members] if members else []
