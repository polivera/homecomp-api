from dataclasses import dataclass, field
from decimal import Decimal
from typing import Self


@dataclass(frozen=True)
class SharedAmount:
    """Value object for monetary amounts (must be non-negative)"""

    value: Decimal
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            if not isinstance(self.value, Decimal):
                raise ValueError(f"Amount must be a Decimal, got {type(self.value)}")
            if self.value < 0:
                raise ValueError(f"Amount must be non-negative, got {self.value}")
            if self.value.as_tuple().exponent < -2:
                raise ValueError(f"Amount cannot have more than 2 decimal places, got {self.value}")

    @classmethod
    def from_float(cls, value: float) -> Self:
        """Create Amount from float value"""
        return cls(Decimal(str(value)))

    @classmethod
    def from_trusted_source(cls, value: Decimal) -> Self:
        """Create Amount from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
