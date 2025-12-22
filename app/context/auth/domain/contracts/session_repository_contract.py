from abc import ABC, abstractmethod
from typing import Optional

from app.context.auth.domain.dto.session_dto import SessionDTO
from app.context.auth.domain.value_objects import (
    AuthUserID,
    SessionToken,
)


class SessionRepositoryContract(ABC):
    @abstractmethod
    async def getSession(
        self, user_id: Optional[AuthUserID] = None, token: Optional[SessionToken] = None
    ) -> Optional[SessionDTO]:
        pass
