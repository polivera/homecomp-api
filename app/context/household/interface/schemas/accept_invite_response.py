from dataclasses import dataclass


@dataclass(frozen=True)
class AcceptInviteResponse:
    member_id: int
    household_id: int
    user_id: int
    role: str
