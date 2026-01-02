from dataclasses import dataclass
from datetime import datetime

from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdName,
    HouseholdUserID,
)


@dataclass(frozen=True)
class HouseholdDTO:
    household_id: HouseholdID | None
    owner_user_id: HouseholdUserID
    name: HouseholdName
    created_at: datetime | None = None
