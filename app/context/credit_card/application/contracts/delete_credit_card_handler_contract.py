from abc import ABC, abstractmethod

from app.context.credit_card.application.commands import DeleteCreditCardCommand
from app.context.credit_card.application.dto import DeleteCreditCardResult


class DeleteCreditCardHandlerContract(ABC):
    """Contract for delete credit card command handler"""

    @abstractmethod
    async def handle(self, command: DeleteCreditCardCommand) -> DeleteCreditCardResult:
        """Handle the delete credit card command"""
        pass
