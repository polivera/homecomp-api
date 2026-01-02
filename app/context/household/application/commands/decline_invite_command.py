from dataclasses import dataclass


@dataclass(frozen=True)
class DeclineInviteCommand:
    """Command to decline a household invitation"""

    user_id: int
    household_id: int
