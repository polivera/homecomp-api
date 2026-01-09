from abc import ABC, abstractmethod

from app.context.category.application.commands import CreateCategoryCommand
from app.context.category.application.dto import CreateCategoryResult


class CreateCategoryHandlerContract(ABC):
    """Contract for create category command handler"""

    @abstractmethod
    async def handle(self, command: CreateCategoryCommand) -> CreateCategoryResult:
        """
        Handle the create category command

        Args:
            command: The create category command

        Returns:
            CreateCategoryResult with the new category ID or error
        """
        pass
