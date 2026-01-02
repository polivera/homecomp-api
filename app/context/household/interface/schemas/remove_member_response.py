from dataclasses import dataclass


@dataclass(frozen=True)
class RemoveMemberResponse:
    success: bool
    message: str
