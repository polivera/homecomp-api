from abc import ABC, abstractmethod

from app.context.household.application.dto import HouseholdMemberResponseDTO
from app.context.household.application.queries import ListHouseholdInvitesQuery


class ListHouseholdInvitesHandlerContract(ABC):
    """Contract for list household invites query handler"""

    @abstractmethod
    async def handle(
        self, query: ListHouseholdInvitesQuery
    ) -> list[HouseholdMemberResponseDTO]:
        """Execute the list household invites query"""
        pass
