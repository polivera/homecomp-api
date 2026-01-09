from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True)
class CategoryColor:
    """Value object for category color (hex color code)"""

    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated and not isinstance(self.value, str):
            raise ValueError(f"CategoryColor must be a string, got {type(self.value)}")
        if not self._validated and len(self.value) != 7:
            raise ValueError(f"CategoryColor must be 7 characters (e.g., #FF5733), got {len(self.value)}")
        if not self._validated and not self.value.startswith("#"):
            raise ValueError(f"CategoryColor must start with #, got {self.value}")
        if not self._validated:
            # Validate hex characters
            try:
                int(self.value[1:], 16)
            except ValueError as err:
                raise ValueError(f"CategoryColor must be a valid hex color code, got {self.value}") from err

    @classmethod
    def from_trusted_source(cls, value: str) -> Self:
        """Create CategoryColor from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
