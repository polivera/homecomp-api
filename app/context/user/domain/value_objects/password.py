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
    def from_plain_text(cls, plain_password: str) -> "Password":
        ph = PasswordHasher()
        return cls(value=ph.hash(plain_password))

    @classmethod
    def from_hash(cls, hashed_password: str) -> "Password":
        return cls(value=hashed_password)

    @classmethod
    def keep_plain(cls, plain_password: str) -> "Password":
        return Password(value=plain_password)

    def verify(self, plain_password: str) -> bool:
        ph = PasswordHasher()
        try:
            return ph.verify(self.value, plain_password)
        except VerifyMismatchError:
            # TODO: Logger here
            return False

    @staticmethod
    def validate(plain_password: str) -> bool:
        return len(plain_password) >= 8
