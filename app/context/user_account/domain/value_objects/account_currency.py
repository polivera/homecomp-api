from dataclasses import dataclass

from app.shared.domain.value_objects.shared_currency import SharedCurrency


@dataclass(frozen=True)
class UserAccountCurrency(SharedCurrency):
    pass
