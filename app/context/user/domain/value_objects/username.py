from dataclasses import dataclass

from app.shared.domain.value_objects import SharedUsername


@dataclass(frozen=True)
class UserName(SharedUsername):
    pass
