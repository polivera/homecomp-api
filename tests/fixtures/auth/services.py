"""Mock services for auth context testing."""

from unittest.mock import AsyncMock

import pytest

from app.context.auth.domain.contracts import LoginServiceContract
from app.context.auth.domain.dto import AuthUserDTO
from app.context.auth.domain.value_objects import AuthPassword, SessionToken


class MockLoginService(LoginServiceContract):
    """Mock implementation of LoginServiceContract for testing."""

    def __init__(self):
        self.handle_mock = AsyncMock()

    async def handle(self, user_password: AuthPassword, db_user: AuthUserDTO) -> SessionToken:
        return await self.handle_mock(user_password=user_password, db_user=db_user)


@pytest.fixture
def mock_login_service():
    """Fixture providing a mock login service."""
    return MockLoginService()
