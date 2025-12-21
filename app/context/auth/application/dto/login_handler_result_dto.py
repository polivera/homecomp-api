from dataclasses import dataclass


@dataclass
class LoginHandlerResultDTO:
    token: str
    error: str
