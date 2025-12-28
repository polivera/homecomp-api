from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.context.household.domain.dto import HouseholdMemberDTO


@dataclass(frozen=True)
class HouseholdMemberResponseDTO:
    """Response DTO for household member information"""

    member_id: int
    household_id: int
    user_id: int
    role: str
    joined_at: Optional[datetime]
    invited_by_user_id: Optional[int]
    invited_at: Optional[datetime]
    household_name: Optional[str] = None
    inviter: Optional[str] = None

    @staticmethod
    def from_domain_dto(member_dto: HouseholdMemberDTO) -> "HouseholdMemberResponseDTO":
        """Convert domain DTO to response DTO"""
        return HouseholdMemberResponseDTO(
            member_id=member_dto.member_id.value if member_dto.member_id else 0,
            household_id=member_dto.household_id.value,
            user_id=member_dto.user_id.value,
            role=member_dto.role.value,
            joined_at=member_dto.joined_at,
            invited_by_user_id=(
                member_dto.invited_by_user_id.value
                if member_dto.invited_by_user_id
                else None
            ),
            invited_at=member_dto.invited_at,
            household_name=member_dto.household_name.value
            if member_dto.household_name
            else None,
            inviter=member_dto.inviter_username.value
            if member_dto.inviter_username
            else None,
        )
