from abc import ABC, abstractmethod


class EventRepositoryContract(ABC):
    """Contract for event repository operations (message queue/outbox pattern)"""

    @abstractmethod
    async def save_event(self):
        """Save event to message queue (outbox table)"""
        pass

    @abstractmethod
    async def get_pending_events(self):
        """Get pending events from message queue"""
        pass

    @abstractmethod
    async def mark_event_completed(self):
        """Mark event as completed"""
        pass

    @abstractmethod
    async def mark_event_failed(self):
        """Mark event as failed"""
        pass
