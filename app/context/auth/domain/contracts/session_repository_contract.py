from abc import ABC, abstractmethod

from app.context.auth.domain.dto.session_dto import SessionDTO
from app.context.auth.domain.value_objects import (
    AuthUserID,
    SessionToken,
)


class SessionRepositoryContract(ABC):
    @abstractmethod
    async def getSession(
        self, user_id: AuthUserID | None = None, token: SessionToken | None = None
    ) -> SessionDTO | None:
        pass

    @abstractmethod
    async def createSession(self, session: SessionDTO) -> SessionDTO:
        """Create a new session."""
        pass

    @abstractmethod
    async def updateSession(self, session: SessionDTO) -> SessionDTO:
        """Update an existing session."""
        pass
