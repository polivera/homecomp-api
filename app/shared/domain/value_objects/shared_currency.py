from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True)
class SharedCurrency:
    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            if not isinstance(self.value, str):
                raise ValueError(f"Currency must be a string, got {type(self.value)}")
            if len(self.value) != 3:
                raise ValueError(
                    f"Currency code must be exactly 3 characters, got {len(self.value)}"
                )
            if not self.value.isalpha():
                raise ValueError(
                    f"Currency code must contain only letters, got {self.value}"
                )
            if not self.value.isupper():
                raise ValueError(f"Currency code must be uppercase, got {self.value}")

    @classmethod
    def from_trusted_source(cls, value: str) -> Self:
        """Create Currency from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
