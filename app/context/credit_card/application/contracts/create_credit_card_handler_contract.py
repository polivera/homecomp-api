from abc import ABC, abstractmethod

from app.context.credit_card.application.commands.create_credit_card_command import (
    CreateCreditCardCommand,
)
from app.context.credit_card.application.dto.create_credit_card_result import (
    CreateCreditCardResult,
)


class CreateCreditCardHandlerContract(ABC):
    """Contract for create credit card command handler"""

    @abstractmethod
    async def handle(
        self, command: CreateCreditCardCommand
    ) -> CreateCreditCardResult:
        """Handle the create credit card command"""
        pass
