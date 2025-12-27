from dataclasses import dataclass

from app.context.user.domain.value_objects.user_id import UserID


@dataclass(frozen=True)
class FindCreditCardsByUserQuery:
    """Query to find all credit cards for a user"""

    user_id: UserID
