from dataclasses import dataclass
from datetime import datetime

from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdMemberID,
    HouseholdName,
    HouseholdRole,
    HouseholdUserID,
)
from app.shared.domain.value_objects import SharedUsername


@dataclass(frozen=True)
class HouseholdMemberDTO:
    """Domain DTO for household member"""

    member_id: HouseholdMemberID | None
    household_id: HouseholdID
    user_id: HouseholdUserID
    role: HouseholdRole
    joined_at: datetime | None = None
    invited_by_user_id: HouseholdUserID | None = None
    invited_at: datetime | None = None
    household_name: HouseholdName | None = None
    inviter_username: SharedUsername | None = None

    @property
    def is_invited(self) -> bool:
        """Check if this is a pending invite (not yet accepted)"""
        return self.joined_at is None

    @property
    def is_active(self) -> bool:
        """Check if this is an active member (accepted and not left)"""
        return self.joined_at is not None
