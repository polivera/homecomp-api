from abc import ABC, abstractmethod

from app.context.household.application.dto import ListUserHouseholdsResult
from app.context.household.application.queries import ListUserHouseholdsQuery


class ListUserHouseholdsHandlerContract(ABC):
    """Contract for list user households query handler"""

    @abstractmethod
    async def handle(self, query: ListUserHouseholdsQuery) -> ListUserHouseholdsResult:
        """Execute the list user households query"""
        pass
