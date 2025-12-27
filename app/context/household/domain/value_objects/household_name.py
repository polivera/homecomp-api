from dataclasses import dataclass, field
from typing_extensions import Self


@dataclass(frozen=True)
class HouseholdName:
    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            if not self.value or not self.value.strip():
                raise ValueError("Household name cannot be empty")
            if len(self.value) > 100:
                raise ValueError(
                    f"Household name cannot exceed 100 characters, got {len(self.value)}"
                )

    @classmethod
    def from_trusted_source(cls, value: str) -> Self:
        """Create HouseholdName from trusted source - skips validation"""
        return cls(value, _validated=True)
