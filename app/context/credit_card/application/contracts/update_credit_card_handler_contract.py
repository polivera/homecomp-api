from abc import ABC, abstractmethod

from app.context.credit_card.application.commands.update_credit_card_command import (
    UpdateCreditCardCommand,
)
from app.context.credit_card.application.dto.update_credit_card_result import (
    UpdateCreditCardResult,
)


class UpdateCreditCardHandlerContract(ABC):
    """Contract for update credit card command handler"""

    @abstractmethod
    async def handle(
        self, command: UpdateCreditCardCommand
    ) -> UpdateCreditCardResult:
        """Handle the update credit card command"""
        pass
