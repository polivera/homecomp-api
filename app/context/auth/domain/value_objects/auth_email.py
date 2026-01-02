from dataclasses import dataclass

from app.shared.domain.value_objects import SharedEmail


@dataclass(frozen=True)
class AuthEmail(SharedEmail):
    pass
