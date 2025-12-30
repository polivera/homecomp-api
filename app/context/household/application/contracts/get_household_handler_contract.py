from abc import ABC, abstractmethod

from app.context.household.application.dto import GetHouseholdResult
from app.context.household.application.queries import GetHouseholdQuery


class GetHouseholdHandlerContract(ABC):
    """Contract for get household query handler"""

    @abstractmethod
    async def handle(self, query: GetHouseholdQuery) -> GetHouseholdResult:
        """Execute the get household query"""
        pass
