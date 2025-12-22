from dataclasses import dataclass


@dataclass(frozen=True)
class LoginHandlerResultDTO:
    token: str
    error: str
