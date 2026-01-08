from abc import ABC, abstractmethod


class SagaRepositoryContract(ABC):
    """Contract for saga state repository operations"""

    @abstractmethod
    async def save_saga(self):
        """Save saga state"""
        pass

    @abstractmethod
    async def get_saga(self):
        """Get saga state by ID"""
        pass

    @abstractmethod
    async def update_saga_status(self):
        """Update saga status"""
        pass
