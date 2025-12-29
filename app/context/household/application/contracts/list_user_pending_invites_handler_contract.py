from abc import ABC, abstractmethod

from app.context.household.application.dto import HouseholdMemberResponseDTO
from app.context.household.application.queries import ListUserPendingInvitesQuery


class ListUserPendingInvitesHandlerContract(ABC):
    """Contract for list user pending invites query handler"""

    @abstractmethod
    async def handle(self, query: ListUserPendingInvitesQuery) -> list[HouseholdMemberResponseDTO]:
        """Execute the list user pending invites query"""
        pass
