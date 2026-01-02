"""Mock handlers for user context testing."""

from unittest.mock import AsyncMock

import pytest

from app.context.user.application.contracts import FindUserHandlerContract
from app.context.user.application.dto import FindUserResult
from app.context.user.application.queries import FindUserQuery


class MockFindUserHandler(FindUserHandlerContract):
    """Mock implementation of FindUserHandlerContract for testing."""

    def __init__(self):
        self.handle_mock = AsyncMock(return_value=None)

    async def handle(self, query: FindUserQuery) -> FindUserResult:
        return await self.handle_mock(query)


@pytest.fixture
def mock_find_user_handler():
    """Fixture providing a mock find user handler."""
    return MockFindUserHandler()
