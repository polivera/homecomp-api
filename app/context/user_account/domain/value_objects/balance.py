from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(frozen=True)
class Balance:
    """Value object for account balance (can be negative for overdrafts)"""

    value: Decimal
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            if not isinstance(self.value, Decimal):
                raise ValueError(f"Balance must be a Decimal, got {type(self.value)}")
            # TODO: Fix this
            if self.value.as_tuple().exponent < -2:
                raise ValueError(
                    f"Balance cannot have more than 2 decimal places, got {self.value}"
                )

    @classmethod
    def from_float(cls, value: float) -> "Balance":
        """Create Balance from float value"""
        return cls(Decimal(str(value)))

    @classmethod
    def from_trusted_source(cls, value: Decimal) -> "Balance":
        """Create Balance from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
