from dataclasses import dataclass, field

from app.context.credit_card.domain.exceptions import (
    InvalidCreditCardNameLengthError,
    InvalidCreditCardNameTypeError,
)


@dataclass(frozen=True)
class CreditCardName:
    """Value object for credit card name"""

    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            if not isinstance(self.value, str):
                raise InvalidCreditCardNameTypeError(
                    f"CreditCardName must be a string, got {type(self.value)}"
                )
            if len(self.value) < 3:
                raise InvalidCreditCardNameLengthError(
                    f"CreditCardName must be at least 3 characters, got {len(self.value)}"
                )
            if len(self.value) > 100:
                raise InvalidCreditCardNameLengthError(
                    f"CreditCardName must be at most 100 characters, got {len(self.value)}"
                )

    @classmethod
    def from_trusted_source(cls, value: str) -> "CreditCardName":
        """Create CreditCardName from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
