from dataclasses import dataclass
from datetime import datetime


@dataclass
class BlockedTime:
    value: datetime

    def toString(self) -> str:
        return self.value.isoformat()

    def isOver(self) -> bool:
        print(self.value.isoformat())
        print(datetime.now().isoformat())
        return self.value < datetime.now()
