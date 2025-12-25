from dataclasses import dataclass, field


@dataclass(frozen=True)
class AccountID:
    """Value object for user account identifier"""

    value: int
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated and not isinstance(self.value, int):
            raise ValueError(f"AccountID must be an integer, got {type(self.value)}")
        if not self._validated and self.value <= 0:
            raise ValueError(f"AccountID must be positive, got {self.value}")

    @classmethod
    def from_trusted_source(cls, value: int) -> "AccountID":
        """Create AccountID from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
