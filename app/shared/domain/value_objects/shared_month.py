from dataclasses import dataclass, field


@dataclass(frozen=True)
class SharedMonth:
    value: int
    _validated: bool = field(default=False, repr=False, compare=False)

    def __post_init__(self):
        """Validate month"""
        if not self._validated:
            if self.value < 1 or self.value > 12:
                raise ValueError("Month must be a value between 1 and 12")
