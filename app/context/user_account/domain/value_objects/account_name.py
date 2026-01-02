from dataclasses import dataclass, field


@dataclass(frozen=True)
class AccountName:
    """Value object for user account name"""

    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated and not isinstance(self.value, str):
            raise ValueError(f"AccountName must be a string, got {type(self.value)}")
        if not self._validated and not self.value.strip():
            raise ValueError("AccountName cannot be empty or whitespace")
        if not self._validated and len(self.value) > 100:
            raise ValueError(f"AccountName cannot exceed 100 characters, got {len(self.value)}")

    @classmethod
    def from_trusted_source(cls, value: str) -> "AccountName":
        """Create AccountName from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
