"""HTTP client fixtures for integration testing.

Provides fixtures for FastAPI test client with database dependency overrides.
"""

from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.shared.infrastructure.database import get_db


@pytest_asyncio.fixture(scope="function")
async def test_client(
    test_db_session: AsyncSession,
) -> AsyncGenerator[AsyncClient]:
    """Create a test client with overridden database dependency."""

    async def override_get_db():
        yield test_db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
