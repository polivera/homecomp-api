from dataclasses import dataclass

from argon2 import PasswordHasher
from argon2.low_level import VerifyMismatchError


@dataclass(frozen=True)
class Password:
    """
    Password value object. It will always represent hashed password in the domain
    """

    value: str

    @classmethod
    def from_plain_text(cls, plainPassword: str) -> "Password":
        ph = PasswordHasher()
        return cls(value=ph.hash(plainPassword))

    def verify(self, plainPassword: str) -> bool:
        ph = PasswordHasher()
        try:
            return ph.verify(self.value, plainPassword)
        except VerifyMismatchError:
            # TODO: Logger here
            return False

    @staticmethod
    def validate(plainPassword: str) -> bool:
        return len(plainPassword) >= 8
