from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, EmailStr


class LoginRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    email: EmailStr
    password: str


@dataclass(frozen=True)
class LoginResponse:
    message: str
