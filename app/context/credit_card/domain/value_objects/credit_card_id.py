from dataclasses import dataclass, field

from app.context.credit_card.domain.exceptions import (
    InvalidCreditCardIdTypeError,
    InvalidCreditCardIdValueError,
)


@dataclass(frozen=True)
class CreditCardID:
    """Value object for credit card identifier"""

    value: int
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated and not isinstance(self.value, int):
            raise InvalidCreditCardIdTypeError(f"CreditCardID must be an integer, got {type(self.value)}")
        if not self._validated and self.value <= 0:
            raise InvalidCreditCardIdValueError(f"CreditCardID must be positive, got {self.value}")

    @classmethod
    def from_trusted_source(cls, value: int) -> "CreditCardID":
        """Create CreditCardID from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
