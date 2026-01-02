from dataclasses import dataclass


@dataclass(frozen=True)
class HouseholdID:
    value: int

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise ValueError(f"HouseholdID must be an integer, got {type(self.value)}")
        if self.value <= 0:
            raise ValueError(f"HouseholdID must be positive, got {self.value}")
