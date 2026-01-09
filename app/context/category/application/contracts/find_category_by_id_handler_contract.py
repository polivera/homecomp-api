from abc import ABC, abstractmethod

from app.context.category.application.dto import FindCategoryByIdResult
from app.context.category.application.queries import FindCategoryByIdQuery


class FindCategoryByIdHandlerContract(ABC):
    """Contract for find category by ID query handler"""

    @abstractmethod
    async def handle(self, query: FindCategoryByIdQuery) -> FindCategoryByIdResult:
        """
        Handle the find category by ID query

        Args:
            query: The find category by ID query

        Returns:
            FindCategoryByIdResult with the category or error
        """
        pass
