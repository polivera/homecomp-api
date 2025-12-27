from dataclasses import dataclass


@dataclass(frozen=True)
class HouseholdUserID:
    value: int

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise ValueError(f"HouseholdUserID must be an integer, got {type(self.value)}")
        if self.value <= 0:
            raise ValueError(f"HouseholdUserID must be positive, got {self.value}")
