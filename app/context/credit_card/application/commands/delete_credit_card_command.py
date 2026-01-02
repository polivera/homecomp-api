from dataclasses import dataclass


@dataclass(frozen=True)
class DeleteCreditCardCommand:
    """Command to delete a credit card"""

    credit_card_id: int
    user_id: int
