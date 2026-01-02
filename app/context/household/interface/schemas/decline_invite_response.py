from dataclasses import dataclass


@dataclass(frozen=True)
class DeclineInviteResponse:
    success: bool
    message: str
