from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation

from app.context.credit_card.domain.exceptions import (
    InvalidCardLimitFormatError,
    InvalidCardLimitPrecisionError,
    InvalidCardLimitTypeError,
    InvalidCardLimitValueError,
)


@dataclass(frozen=True)
class CardLimit:
    """Value object for credit card limit"""

    value: Decimal
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            if not isinstance(self.value, Decimal):
                raise InvalidCardLimitTypeError(f"CardLimit must be a Decimal, got {type(self.value)}")
            if self.value <= 0:
                raise InvalidCardLimitValueError(f"CardLimit must be positive, got {self.value}")

            # Check for max 2 decimal places
            if self.value.as_tuple().exponent < -2:
                raise InvalidCardLimitPrecisionError(f"CardLimit must have at most 2 decimal places, got {self.value}")

    @classmethod
    def from_float(cls, value: float) -> "CardLimit":
        """Create CardLimit from float value"""
        try:
            # Round to 2 decimal places
            decimal_value = Decimal(str(value)).quantize(Decimal("0.01"))
            return cls(decimal_value)
        except (InvalidOperation, ValueError) as e:
            raise InvalidCardLimitFormatError(f"Invalid CardLimit value: {value}") from e

    @classmethod
    def from_trusted_source(cls, value: Decimal) -> "CardLimit":
        """Create CardLimit from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
