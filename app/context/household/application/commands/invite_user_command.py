from dataclasses import dataclass


@dataclass(frozen=True)
class InviteUserCommand:
    """Command to invite a user to a household"""

    inviter_user_id: int
    household_id: int
    invitee_user_id: int
    role: str
