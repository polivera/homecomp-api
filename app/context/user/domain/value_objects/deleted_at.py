from dataclasses import dataclass

from app.shared.domain.value_objects import SharedDeletedAt


@dataclass(frozen=True)
class UserDeletedAt(SharedDeletedAt):
    pass
