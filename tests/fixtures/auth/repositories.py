"""Mock repositories for auth context testing."""

from unittest.mock import AsyncMock

import pytest

from app.context.auth.domain.contracts import SessionRepositoryContract
from app.context.auth.domain.dto.session_dto import SessionDTO
from app.context.auth.domain.value_objects import AuthUserID, SessionToken


class MockSessionRepository(SessionRepositoryContract):
    """Mock implementation of SessionRepositoryContract for testing."""

    def __init__(self):
        self.get_session_mock = AsyncMock(return_value=None)
        self.create_session_mock = AsyncMock()
        self.update_session_mock = AsyncMock()

    async def getSession(
        self, user_id: AuthUserID | None = None, token: SessionToken | None = None
    ) -> SessionDTO | None:
        return await self.get_session_mock(user_id=user_id, token=token)

    async def createSession(self, session: SessionDTO) -> SessionDTO:
        return await self.create_session_mock(session)

    async def updateSession(self, session: SessionDTO) -> SessionDTO:
        return await self.update_session_mock(session)


@pytest.fixture
def mock_session_repository():
    """Fixture providing a mock session repository."""
    return MockSessionRepository()
