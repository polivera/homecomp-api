from dataclasses import dataclass

from app.shared.domain.value_objects import SharedPassword


@dataclass(frozen=True)
class AuthPassword(SharedPassword):
    pass
