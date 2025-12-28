from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class HouseholdMemberResponse:
    """Response schema for household member/invite information"""

    member_id: int
    household_id: int
    user_id: int
    role: str
    joined_at: Optional[datetime]
    invited_by_user_id: Optional[int]
    invited_at: Optional[datetime]
    household_name: Optional[str]
    inviter: Optional[str]
