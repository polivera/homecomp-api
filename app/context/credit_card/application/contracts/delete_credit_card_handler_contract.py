from abc import ABC, abstractmethod

from app.context.credit_card.application.commands.delete_credit_card_command import (
    DeleteCreditCardCommand,
)


class DeleteCreditCardHandlerContract(ABC):
    """Contract for delete credit card command handler"""

    @abstractmethod
    async def handle(self, command: DeleteCreditCardCommand) -> bool:
        """Handle the delete credit card command. Returns True if deleted, False otherwise"""
        pass
