"""Event occurrence timestamp value object"""

from dataclasses import dataclass

from app.shared.domain.value_objects.shared_date import SharedDateTime


@dataclass(frozen=True)
class OccurredAt(SharedDateTime):
    """UTC timestamp when a domain event occurred"""

    pass
