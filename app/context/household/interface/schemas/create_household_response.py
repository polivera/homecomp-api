from dataclasses import dataclass


@dataclass(frozen=True)
class CreateHouseholdResponse:
    id: int
    name: str
