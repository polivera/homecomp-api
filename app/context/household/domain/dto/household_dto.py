from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdName,
    HouseholdUserID,
)


@dataclass(frozen=True)
class HouseholdDTO:
    household_id: Optional[HouseholdID]
    owner_user_id: HouseholdUserID
    name: HouseholdName
    created_at: Optional[datetime] = None
