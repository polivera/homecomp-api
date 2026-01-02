from dataclasses import dataclass

from app.shared.domain.value_objects import SharedCurrency


@dataclass(frozen=True)
class CreditCardCurrency(SharedCurrency):
    pass
