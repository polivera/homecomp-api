from dataclasses import dataclass


@dataclass(frozen=True)
class HouseholdMemberID:
    value: int

    def __post_init__(self):
        if not isinstance(self.value, int):
            raise ValueError("Household member ID must be an integer")
        if self.value <= 0:
            raise ValueError("Household member ID must be a positive integer")
