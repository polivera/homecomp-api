from abc import ABC, abstractmethod
from collections.abc import Callable

from app.shared.domain.dto import DomainEventDTO


class EventBusContract(ABC):
    """Contract for publishing and subscribing to domain events"""

    @abstractmethod
    async def publish(self, event: DomainEventDTO) -> None:
        """Publish an event to all subscribers"""
        pass

    @abstractmethod
    def subscribe(self, event_type: type[DomainEventDTO], handler: Callable[[DomainEventDTO], None]) -> None:
        """Register a handler for a specific event type"""
        pass
