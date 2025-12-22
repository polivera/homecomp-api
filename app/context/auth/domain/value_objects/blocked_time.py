from dataclasses import dataclass
from datetime import datetime


@dataclass
class BlockedTime:
    value: datetime

    def toString(self) -> str:
        return self.value.isoformat()

    def isOver(self) -> bool:
        return self.value > datetime.now()
