from dataclasses import dataclass

from app.shared.domain.value_objects.shared_balance import SharedBalance


@dataclass(frozen=True)
class UserAccountBalance(SharedBalance):
    pass
