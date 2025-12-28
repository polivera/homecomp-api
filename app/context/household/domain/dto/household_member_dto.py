from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.context.household.domain.value_objects import (
    HouseholdID,
    HouseholdMemberID,
    HouseholdRole,
    HouseholdUserID,
)


@dataclass(frozen=True)
class HouseholdMemberDTO:
    """Domain DTO for household member"""

    member_id: Optional[HouseholdMemberID]
    household_id: HouseholdID
    user_id: HouseholdUserID
    role: HouseholdRole
    joined_at: Optional[datetime] = None
    left_at: Optional[datetime] = None
    invited_by_user_id: Optional[HouseholdUserID] = None
    invited_at: Optional[datetime] = None

    @property
    def is_invited(self) -> bool:
        """Check if this is a pending invite (not yet accepted)"""
        return self.joined_at is None and self.left_at is None

    @property
    def is_active(self) -> bool:
        """Check if this is an active member (accepted and not left)"""
        return self.joined_at is not None and self.left_at is None

    @property
    def has_left(self) -> bool:
        """Check if the member has left the household"""
        return self.left_at is not None

    @property
    def has_declined(self) -> bool:
        """Check if the invite was declined (left without joining)"""
        return self.left_at is not None and self.joined_at is None
