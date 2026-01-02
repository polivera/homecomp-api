"""User fixtures for integration testing.

Provides fixtures for creating test users in the database.
"""

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.context.user.infrastructure.models import UserModel
from app.shared.domain.value_objects import SharedPassword


@pytest_asyncio.fixture
async def test_user(test_db_session: AsyncSession) -> dict:
    """Create a test user in the database.

    Returns:
        dict with user credentials and id:
            - email: str
            - password: str (plain text for testing)
            - user_id: int
            - hashed_password: str
    """
    email = "testuser@example.com"
    password = "SecurePassword123!"
    hashed_password = SharedPassword.from_plain_text(password).value

    user = UserModel(
        email=email,
        password=hashed_password,
        username="testuser",
    )

    test_db_session.add(user)
    await test_db_session.commit()
    await test_db_session.refresh(user)

    return {
        "email": email,
        "password": password,
        "user_id": user.id,
        "hashed_password": hashed_password,
    }


@pytest_asyncio.fixture
async def blocked_user(test_db_session: AsyncSession) -> dict:
    """Create a blocked user (multiple failed login attempts).

    Note: This is a placeholder. Actual blocking mechanism depends on
    the login throttling implementation (in-memory or Redis-based).
    """
    email = "blocked@example.com"
    password = "BlockedPassword123!"
    hashed_password = SharedPassword.from_plain_text(password).value

    user = UserModel(
        email=email,
        password=hashed_password,
        username="blockeduser",
    )

    test_db_session.add(user)
    await test_db_session.commit()
    await test_db_session.refresh(user)

    return {
        "email": email,
        "password": password,
        "user_id": user.id,
        "hashed_password": hashed_password,
    }
