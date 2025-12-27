from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Optional, Self


@dataclass(frozen=True)
class SharedDeletedAt:
    """
    DeletedAt value object for soft delete functionality.
    Represents the timestamp when an entity was marked as deleted.
    """

    value: datetime
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        """Validate that deleted_at is not in the future."""
        if not self._validated:
            if not isinstance(self.value, datetime):
                raise ValueError("DeletedAt must be a datetime object")

            # Ensure timezone-aware comparison
            now = datetime.now(UTC)
            value_utc = self.value if self.value.tzinfo else self.value.replace(tzinfo=UTC)

            if value_utc > now:
                raise ValueError("DeletedAt cannot be in the future")

    @classmethod
    def now(cls) -> Self:
        """Create a DeletedAt timestamp for the current moment (UTC)."""
        return cls(value=datetime.now(UTC), _validated=True)

    @classmethod
    def from_trusted_source(cls, value: datetime) -> Self:
        """
        Create DeletedAt from trusted source (e.g., database) - skips validation.
        Use this to avoid performance overhead when data is already validated.
        """
        return cls(value=value, _validated=True)

    @classmethod
    def from_optional(cls, value: Optional[datetime]) -> Optional[Self]:
        """
        Create DeletedAt from optional datetime.
        Returns None if value is None (entity is not deleted).
        """
        if value is None:
            return None
        return cls.from_trusted_source(value)
