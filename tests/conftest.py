from typing import Optional
from unittest.mock import AsyncMock

import pytest

from app.context.auth.domain.contracts import (
    LoginServiceContract,
    SessionRepositoryContract,
)
from app.context.auth.domain.dto import AuthUserDTO
from app.context.auth.domain.dto.session_dto import SessionDTO
from app.context.auth.domain.value_objects import AuthPassword, AuthUserID, SessionToken
from app.context.user.application.contracts import FindUserHandlerContract
from app.context.user.application.dto import UserContextDTO
from app.context.user.application.queries import FindUserQuery


class MockSessionRepository(SessionRepositoryContract):
    """Mock implementation of SessionRepositoryContract for testing."""

    def __init__(self):
        self.get_session_mock = AsyncMock(return_value=None)
        self.create_session_mock = AsyncMock()
        self.update_session_mock = AsyncMock()

    async def getSession(
        self, user_id: Optional[AuthUserID] = None, token: Optional[SessionToken] = None
    ) -> Optional[SessionDTO]:
        return await self.get_session_mock(user_id=user_id, token=token)

    async def createSession(self, session: SessionDTO) -> SessionDTO:
        return await self.create_session_mock(session)

    async def updateSession(self, session: SessionDTO) -> SessionDTO:
        return await self.update_session_mock(session)


@pytest.fixture
def mock_session_repository():
    """Fixture providing a mock session repository."""
    return MockSessionRepository()


class MockFindUserHandler(FindUserHandlerContract):
    """Mock implementation of FindUserHandlerContract for testing."""

    def __init__(self):
        self.handle_mock = AsyncMock(return_value=None)

    async def handle(self, query: FindUserQuery) -> Optional[UserContextDTO]:
        return await self.handle_mock(query)


@pytest.fixture
def mock_find_user_handler():
    """Fixture providing a mock find user handler."""
    return MockFindUserHandler()


class MockLoginService(LoginServiceContract):
    """Mock implementation of LoginServiceContract for testing."""

    def __init__(self):
        self.handle_mock = AsyncMock()

    async def handle(
        self, user_password: AuthPassword, db_user: AuthUserDTO
    ) -> SessionToken:
        return await self.handle_mock(user_password=user_password, db_user=db_user)


@pytest.fixture
def mock_login_service():
    """Fixture providing a mock login service."""
    return MockLoginService()
