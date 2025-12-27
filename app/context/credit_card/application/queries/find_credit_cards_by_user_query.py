from dataclasses import dataclass


@dataclass(frozen=True)
class FindCreditCardsByUserQuery:
    """Query to find all credit cards for a user"""

    user_id: int
