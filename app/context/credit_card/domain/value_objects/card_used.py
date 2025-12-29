from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation

from app.context.credit_card.domain.exceptions import (
    InvalidCardUsedFormatError,
    InvalidCardUsedPrecisionError,
    InvalidCardUsedTypeError,
    InvalidCardUsedValueError,
)


@dataclass(frozen=True)
class CardUsed:
    """Value object for credit card used amount"""

    value: Decimal
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            if not isinstance(self.value, Decimal):
                raise InvalidCardUsedTypeError(f"CardUsed must be a Decimal, got {type(self.value)}")
            if self.value < 0:
                raise InvalidCardUsedValueError(f"CardUsed must be non-negative, got {self.value}")

            # Check for max 2 decimal places
            if self.value.as_tuple().exponent < -2:
                raise InvalidCardUsedPrecisionError(f"CardUsed must have at most 2 decimal places, got {self.value}")

    @classmethod
    def from_float(cls, value: float) -> "CardUsed":
        """Create CardUsed from float value"""
        try:
            # Round to 2 decimal places
            decimal_value = Decimal(str(value)).quantize(Decimal("0.01"))
            return cls(decimal_value)
        except (InvalidOperation, ValueError) as e:
            raise InvalidCardUsedFormatError(f"Invalid CardUsed value: {value}") from e

    @classmethod
    def from_trusted_source(cls, value: Decimal) -> "CardUsed":
        """Create CardUsed from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
