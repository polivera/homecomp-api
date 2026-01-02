from dataclasses import dataclass

from app.shared.domain.value_objects import SharedUserID


@dataclass(frozen=True)
class CreditCardUserID(SharedUserID):
    pass
