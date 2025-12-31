from dataclasses import dataclass, field


@dataclass(frozen=True)
class EntryDescription:
    """Value object for entry description"""

    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated and not isinstance(self.value, str):
            raise ValueError(f"EntryDescription must be a string, got {type(self.value)}")
        if not self._validated and len(self.value) > 500:
            raise ValueError(f"EntryDescription cannot exceed 500 characters, got {len(self.value)}")

    @classmethod
    def from_trusted_source(cls, value: str) -> "EntryDescription":
        """Create EntryDescription from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
