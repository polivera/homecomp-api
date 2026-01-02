from dataclasses import dataclass


@dataclass(frozen=True)
class CreateHouseholdCommand:
    user_id: int
    name: str
