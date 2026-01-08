from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.shared.domain.dto import DomainEventDTO

TEvent = TypeVar("TEvent", bound=DomainEventDTO)


class EventHandlerContract(ABC, Generic[TEvent]):
    @abstractmethod
    async def handle(self, event: TEvent) -> None:
        pass

    @abstractmethod
    async def compensate(self, event: TEvent) -> None:
        pass
