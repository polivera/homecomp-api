from dataclasses import dataclass
from pydantic import BaseModel, EmailStr, ConfigDict


class LoginRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    email: EmailStr
    password: str


@dataclass(frozen=True)
class LoginResponse:
    token: str
