from dataclasses import dataclass, field

from typing_extensions import Self


@dataclass(frozen=True)
class HouseholdRole:
    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    # Only role available for now is participant
    VALID_ROLES = {"participant"}

    def __post_init__(self):
        if not self._validated:
            if not self.value:
                raise ValueError("Role cannot be empty")
            if self.value not in self.VALID_ROLES:
                raise ValueError(
                    f"Invalid role: '{self.value}'. Must be one of {self.VALID_ROLES}"
                )

    @classmethod
    def from_trusted_source(cls, value: str) -> Self:
        """Create role from trusted source (e.g., database) - skips validation"""
        return cls(value, _validated=True)
