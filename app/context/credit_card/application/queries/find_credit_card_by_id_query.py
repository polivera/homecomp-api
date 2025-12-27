from dataclasses import dataclass


@dataclass(frozen=True)
class FindCreditCardByIdQuery:
    """Query to find a credit card by ID"""

    credit_card_id: int
    user_id: int
