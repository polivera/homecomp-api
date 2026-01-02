from dataclasses import dataclass


@dataclass(frozen=True)
class AcceptInviteCommand:
    """Command to accept a household invitation"""

    user_id: int
    household_id: int
