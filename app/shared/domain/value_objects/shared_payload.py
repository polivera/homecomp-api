from dataclasses import dataclass, field
from typing import Any, Self


@dataclass(frozen=True)
class SharedPayload:
    """Shared payload value object for JSON data storage."""

    value: dict[str, Any]
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        """Validate payload unless loaded from trusted source."""
        if not self._validated:
            if not isinstance(self.value, dict):
                raise ValueError(f"Payload must be a dict, got {type(self.value).__name__}")

            if not self.value:
                raise ValueError("Payload cannot be empty")

    @classmethod
    def from_trusted_source(cls, payload: dict[str, Any]) -> Self:
        return cls(value=payload, _validated=True)

    @classmethod
    def empty(cls) -> Self:
        """Create empty payload"""
        return cls.from_trusted_source({})

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from payload"""
        return self.value.get(key, default)
