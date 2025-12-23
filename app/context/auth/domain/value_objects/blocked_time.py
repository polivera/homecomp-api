from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Final, Self


@dataclass
class BlockedTime:
    value: datetime

    BLOCK_MINUTES: Final = 15

    def toString(self) -> str:
        return self.value.isoformat()

    def isOver(self) -> bool:
        return self.value < datetime.now()

    @classmethod
    def setBlocked(cls) -> Self:
        return cls(datetime.now() + timedelta(minutes=cls.BLOCK_MINUTES))
