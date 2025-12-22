import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SharedEmail:
    value: str

    def __post_init__(self):
        if not self.value or not isinstance(self.value, str):
            raise ValueError("Email cannot be empty")

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, self.value):
            raise ValueError(f"Invalid email format: {self.value}")
