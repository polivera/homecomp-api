from dataclasses import dataclass

from app.context.household.interface.schemas.household_response import HouseholdResponse


@dataclass(frozen=True)
class ListHouseholdsResponse:
    """Response for list households endpoint"""

    households: list[HouseholdResponse]
