from dataclasses import dataclass

from app.shared.domain.value_objects.shared_account_id import SharedAccountID


@dataclass(frozen=True)
class UserAccountID(SharedAccountID):
    pass
