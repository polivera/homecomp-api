import re
from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True)
class SharedEmail:
    value: str
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        if not self._validated:
            if not self.value or not isinstance(self.value, str):
                raise ValueError("Email cannot be empty")

            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_pattern, self.value):
                raise ValueError(f"Invalid email format: {self.value}")

    @classmethod
    def from_trusted_source(cls, value: str) -> Self:
        """
        Create Email from trusted source (e.g., database) - skips validation.
        Use this to avoid performance overhead when data is already validated.
        """
        return cls(value, _validated=True)
