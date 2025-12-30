from app.context.household.application.contracts import (
    ListUserPendingInvitesHandlerContract,
)
from app.context.household.application.dto import HouseholdMemberResponseDTO
from app.context.household.application.queries import ListUserPendingInvitesQuery
from app.context.household.domain.contracts import HouseholdRepositoryContract
from app.context.household.domain.value_objects import HouseholdUserID
from app.shared.domain.contracts import LoggerContract


class ListUserPendingInvitesHandler(ListUserPendingInvitesHandlerContract):
    """Handler for list user pending invites query"""

    def __init__(self, repository: HouseholdRepositoryContract, logger: LoggerContract):
        self._repository = repository
        self._logger = logger

    async def handle(self, query: ListUserPendingInvitesQuery) -> list[HouseholdMemberResponseDTO]:
        """Execute the list user pending invites query"""

        self._logger.debug("Handling list user pending invites query", user_id=query.user_id)

        members = await self._repository.list_user_pending_household_invites(
            user_id=HouseholdUserID(query.user_id),
        )

        return [HouseholdMemberResponseDTO.from_domain_dto(member) for member in members] if members else []
