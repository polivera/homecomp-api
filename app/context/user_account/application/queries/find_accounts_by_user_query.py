from dataclasses import dataclass

from app.context.user.domain.value_objects.user_id import UserID


@dataclass(frozen=True)
class FindAccountsByUserQuery:
    user_id: UserID
