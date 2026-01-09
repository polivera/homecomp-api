from abc import ABC, abstractmethod

from app.context.category.application.commands import UpdateCategoryCommand
from app.context.category.application.dto import UpdateCategoryResult


class UpdateCategoryHandlerContract(ABC):
    """Contract for update category command handler"""

    @abstractmethod
    async def handle(self, command: UpdateCategoryCommand) -> UpdateCategoryResult:
        """
        Handle the update category command

        Args:
            command: The update category command

        Returns:
            UpdateCategoryResult with the updated category or error
        """
        pass
