from abc import ABC, abstractmethod

from app.context.category.application.commands import DeleteCategoryCommand
from app.context.category.application.dto import DeleteCategoryResult


class DeleteCategoryHandlerContract(ABC):
    """Contract for delete category command handler"""

    @abstractmethod
    async def handle(self, command: DeleteCategoryCommand) -> DeleteCategoryResult:
        """
        Handle the delete category command

        Args:
            command: The delete category command

        Returns:
            DeleteCategoryResult with success status or error
        """
        pass
