from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class HouseholdMemberResponse:
    """Response schema for household member/invite information"""

    member_id: int
    household_id: int
    user_id: int
    role: str
    joined_at: datetime | None
    invited_by_user_id: int | None
    invited_at: datetime | None
    household_name: str | None
    inviter: str | None
