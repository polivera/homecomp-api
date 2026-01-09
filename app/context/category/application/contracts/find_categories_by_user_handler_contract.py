from abc import ABC, abstractmethod

from app.context.category.application.dto import FindCategoriesByUserResult
from app.context.category.application.queries import FindCategoriesByUserQuery


class FindCategoriesByUserHandlerContract(ABC):
    """Contract for find categories by user query handler"""

    @abstractmethod
    async def handle(self, query: FindCategoriesByUserQuery) -> FindCategoriesByUserResult:
        """
        Handle the find categories by user query

        Args:
            query: The find categories by user query

        Returns:
            FindCategoriesByUserResult with the list of categories or error
        """
        pass
